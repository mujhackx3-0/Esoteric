
import unittest
from unittest.mock import patch
from main import State, loan_sales_agent_graph, HumanMessage

class TestIntegration(unittest.TestCase):
    """Integration tests for the LangGraph state machine in main.py."""

    @patch("main.llm_with_loan_tools")
    def test_full_loan_application_flow(self, mock_llm):
        """
        Tests the full loan application flow from start to finish.
        """
        # Mock the LLM's responses to simulate a conversation
        mock_llm.invoke.side_effect = [
            {"content": "I need a loan of 100000 for a car."},
            {"content": "My name is John Doe."},
            {"content": "Yes, please proceed with KYC."},
            {"content": "Yes, please proceed with the credit check."},
            {"content": "Yes, I accept the offer."},
        ]

        chatbot = loan_sales_agent_graph()
        config = {"configurable": {"thread_id": "_loan_sales_session_test"}}
        initial_state = State()

        # 1. Initial greeting
        current_state = chatbot.invoke(initial_state, config=config)
        self.assertEqual(len(current_state.messages), 1)
        self.assertEqual(current_state.messages[0].type, "ai")

        # 2. User provides loan details
        current_state.messages.append(HumanMessage(content="I need a loan of 100000 for a car."))
        current_state = chatbot.invoke(current_state, config=config)
        self.assertEqual(current_state.current_loan_application.desired_amount, 100000)
        self.assertEqual(current_state.current_loan_application.purpose, "car")

        # 3. User provides name
        current_state.messages.append(HumanMessage(content="My name is John Doe."))
        current_state = chatbot.invoke(current_state, config=config)
        self.assertEqual(current_state.current_loan_application.applicant_name, "John Doe")

        # 4. User agrees to KYC
        current_state.messages.append(HumanMessage(content="Yes, please proceed with KYC."))
        current_state = chatbot.invoke(current_state, config=config)
        self.assertTrue(current_state.current_loan_application.kyc_verified)

        # 5. User agrees to credit check
        current_state.messages.append(HumanMessage(content="Yes, please proceed with the credit check."))
        current_state = chatbot.invoke(current_state, config=config)
        self.assertIn(current_state.current_loan_application.credit_eligibility, ["eligible", "not_eligible"])

        # 6. User accepts offer
        if current_state.current_loan_application.credit_eligibility == "eligible":
            current_state.messages.append(HumanMessage(content="Yes, I accept the offer."))
            current_state = chatbot.invoke(current_state, config=config)
            self.assertTrue(current_state.current_loan_application.sanction_letter_generated)

if __name__ == "__main__":
    unittest.main()
