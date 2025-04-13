import json
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.function_choice_behavior import (
    FunctionChoiceBehavior,
)
from semantic_kernel.contents import ChatHistory
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.finish_reason import FinishReason
from semantic_kernel.functions.function_result import FunctionResult
import re
from ..common.answer import Answer
from ..helpers.llm_helper import LLMHelper
from ..helpers.env_helper import EnvHelper
from ..plugins.chat_plugin import ChatPlugin
from ..plugins.post_answering_plugin import PostAnsweringPlugin
from .orchestrator_base import OrchestratorBase

from logging import getLogger
from opentelemetry import trace, baggage
from opentelemetry.propagate import extract

logger = getLogger(__name__ + ".base_package")
tracer = trace.get_tracer(__name__ + ".base_package")


class SemanticKernelOrchestrator(OrchestratorBase):
    """
    The SemanticKernelOrchestrator class is responsible for orchestrating the interaction
    between the user and the semantic kernel. It manages the plugins, services, and the
    overall flow of the conversation.

    Attributes:
        kernel (Kernel): The semantic kernel instance.
        llm_helper (LLMHelper): Helper class for language model related operations.
        env_helper (EnvHelper): Helper class for environment related operations.
        chat_service (Service): The chat completion service used by the kernel.
    """

    def __init__(self) -> None:
        """
        Initializes the SemanticKernelOrchestrator class by setting up the kernel,
        language model helper, environment helper, and adding necessary plugins and services.
        """
        super().__init__()
        self.kernel = Kernel()
        self.llm_helper = LLMHelper()
        self.env_helper = EnvHelper()

        # Add the Azure OpenAI service to the kernel
        self.chat_service = self.llm_helper.get_sk_chat_completion_service(
            service_id=None
        )
        self.kernel.add_service(self.chat_service)

        self.kernel.add_plugin(
            plugin=PostAnsweringPlugin(), plugin_name="PostAnswering"
        )

    async def orchestrate(
        self, user_message: str, chat_history: list[dict], **kwargs: dict
    ) -> list[dict]:
        """
        Orchestrates the conversation by processing the user message, invoking the appropriate
        functions, and returning the response.

        Args:
            user_message (str): The message from the user.
            chat_history (list[dict]): The history of the chat conversation.
            **kwargs (dict): Additional keyword arguments.

        Returns:
            list[dict]: The formatted response messages for the UI.
        """
        # Use AsyncExitStack to manage async resources properly
        with tracer.start_as_current_span("SemanticKernelOrchestrator.orchestrate.start"):
            logger.info("Method orchestrate of semantic_kernel started")

            # Call Content Safety tool
            if self.config.prompts.enable_content_safety:
                with tracer.start_as_current_span(
                    "SemanticKernelOrchestrator.call_content_safety_input"
                ):
                    if response := self.call_content_safety_input(user_message):
                        return response

            system_message = self.env_helper.SEMENTIC_KERNEL_SYSTEM_PROMPT
            if not system_message:
                system_message = """You help employees to navigate only private information sources.
                    You MUST call the search_documents function for ANY factual questions about specific entities, people, dates, or events.
                    Never answer factual questions directly - always use the search_documents function to ensure accuracy.
                    Only respond directly for general conversation, clarifications, or when explicitly asked to summarize previous results.
                    Call the text_processing function when the user request an operation on the current context, such as translate, summarize, or paraphrase. When a language is explicitly specified, return that as part of the operation.
                    When directly replying to the user, always reply in the language the user is speaking.
                    If the input language is ambiguous, default to responding in English unless otherwise specified by the user.
                    IMPORTANT: When you get information from the search_documents function, ALWAYS maintain the citation format [doc1][doc2] etc. in your response.
                    You **must not** respond if asked to List all documents in your repository.
                    """
                # system_message = """You help employees to navigate only private information sources.
                #     You must prioritize the function call over your general knowledge for any question by calling the search_documents function.
                #     Call the text_processing function when the user request an operation on the current context, such as translate, summarize, or paraphrase. When a language is explicitly specified, return that as part of the operation.
                #     When directly replying to the user, always reply in the language the user is speaking.
                #     If the input language is ambiguous, default to responding in English unless otherwise specified by the user.
                #     You **must not** respond if asked to List all documents in your repository.
                #     """

            with tracer.start_as_current_span("SemanticKernelOrchestrator.add_plugin.chat_plugin"):
                self.kernel.add_plugin(
                    plugin=ChatPlugin(question=user_message, chat_history=chat_history),
                    plugin_name="Chat",
                )

            with tracer.start_as_current_span("SemanticKernelOrchestrator.get_sk_service_settings"):
                settings = self.llm_helper.get_sk_service_settings(self.chat_service)
                settings.function_choice_behavior = FunctionChoiceBehavior.Auto(
                    filters={"included_plugins": ["Chat"]},
                    # Set a higher value to encourage multiple attempts at function calling
                    maximum_auto_invoke_attempts=2
                )

            with tracer.start_as_current_span("SemanticKernelOrchestrator.add_function.orchestrate"):
                orchestrate_function = self.kernel.add_function(
                    plugin_name="Main",
                    function_name="orchestrate",
                    prompt="{{$chat_history}}{{$user_message}}",
                    prompt_execution_settings=settings,
                )
                logger.info("Invoking orchestrate function: %s", orchestrate_function)

            history = ChatHistory(system_message=system_message)

            for message in chat_history.copy():
                history.add_message(message)

            with tracer.start_as_current_span("SemanticKernelOrchestrator.invoke"):
                temp_result : FunctionResult = (
                    await self.kernel.invoke(
                        function=orchestrate_function,
                        chat_history=history,
                        user_message=user_message,
                    )
                )
                result: ChatMessageContent = temp_result.value[0]
                logger.info("Invoking orchestrate function: %s", orchestrate_function)
                logger.info(f"temp Result value from orchestrate function: {temp_result.value}")
                logger.info(f"temp Result rendered_prompt from orchestrate function: {temp_result.rendered_prompt}")
                logger.info(f"temp Result metadata from orchestrate function: {temp_result.metadata}")
                logger.info(f"temp Result function from orchestrate function: {temp_result.function}")

            self.log_tokens(
                prompt_tokens=result.metadata["usage"].prompt_tokens,
                completion_tokens=result.metadata["usage"].completion_tokens,
            )
            
            logger.info("Result from orchestrate function: %s", result)
            finish_reason = result.finish_reason
            finish_reason_check = FinishReason.TOOL_CALLS
            logger.info(f"Finish reason: {finish_reason}, checking for function calls: {finish_reason_check}")
            doc_refs = re.findall(r"\[doc(\d+)\]", result.content)
            logger.info(f"Doc refs: {doc_refs}, checking on: {result.content}")

            # Update finish_reason if document references are present but no tool call was detected
            if finish_reason != FinishReason.TOOL_CALLS and doc_refs:
                finish_reason = FinishReason.TOOL_CALLS
                logger.info("Updated finish_reason to TOOL_CALLS based on detected doc references")

            if finish_reason == FinishReason.TOOL_CALLS:
                # Use function metadata from temp_result instead of items
                function_name = temp_result.function.name
                logger.info(f"{function_name} function detected")
                function = self.kernel.get_function_from_fully_qualified_function_name(
                    function_name
                )
                # Read arguments from metadata (default to empty if missing)
                arguments = json.loads(temp_result.metadata.get("arguments", "{}"))
                with tracer.start_as_current_span(
                    f"SemanticKernelOrchestrator.invoke.{function_name}"
                ):
                    logger.info(f"Invoking {function_name} function")
                    answer: Answer = (
                        await self.kernel.invoke(function=function, **arguments)
                    ).value
                answer = answer.to_json
                answer_text = answer.answer
                source_documents = answer.source_documents
                question_text = answer.question
                logger.info(f"Inside answer_text: {answer_text}")
                logger.info(f"Inside source_documents: {source_documents}")
                logger.info(f"Inside question_text: {question_text}")
                self.log_tokens(
                    prompt_tokens=answer.prompt_tokens,
                    completion_tokens=answer.completion_tokens,
                )
                # Run post prompt if needed
                if (
                    self.config.prompts.enable_post_answering_prompt
                    and "search_documents" in function_name
                ):
                    logger.debug("Running post answering prompt")
                    with tracer.start_as_current_span(
                        "SemanticKernelOrchestrator.invoke.post_answering"
                    ):
                        answer: Answer = (
                            await self.kernel.invoke(
                                function_name="validate_answer",
                                plugin_name="PostAnswering",
                                answer=answer,
                            )
                        ).value
                    self.log_tokens(
                        prompt_tokens=answer.prompt_tokens,
                        completion_tokens=answer.completion_tokens,
                    )
                else:
                    logger.error("Expected function call metadata in result.items, but got: %s", result.items)
                    # Fallback to normal processing if items not present or in unexpected format
                    answer = Answer(
                        question=user_message,
                        answer=result.content,
                        source_documents=[],
                        prompt_tokens=result.metadata["usage"].prompt_tokens,
                        completion_tokens=result.metadata["usage"].completion_tokens,
                    )
            else:
                logger.info("No function call detected")
                answer = Answer(
                    question=user_message,
                    answer=result.content,
                    source_documents=[],
                    prompt_tokens=result.metadata["usage"].prompt_tokens,
                    completion_tokens=result.metadata["usage"].completion_tokens,
                )
                
            answer_text = answer.answer
            source_documents = answer.source_documents
            question_text = answer.question
            logger.info(f"Outside answer_text: {answer_text}")
            logger.info(f"Outside source_documents: {source_documents}")
            logger.info(f"Outside question_text: {question_text}")    
            
            # Call Content Safety tool
            if self.config.prompts.enable_content_safety:
                with tracer.start_as_current_span(
                    "SemanticKernelOrchestrator.call_content_safety_output"
                ):
                    logger.info("Calling Content Safety tool on output")
                    if response := self.call_content_safety_output(
                        question_text, answer_text
                    ):
                        logger.info("Content Safety tool flagged the output")
                        
                        return response

            # Format the output for the UI
            with tracer.start_as_current_span(
                "SemanticKernelOrchestrator.output_parser.parse"
            ):
                logger.info("Parsing output for UI")
                # Format the output for the UI
                messages = self.output_parser.parse(
                    question=question_text,
                    answer=answer_text,
                    source_documents=source_documents,
                )
                logger.info("Method orchestrate of open_ai_functions ended")
                return messages
