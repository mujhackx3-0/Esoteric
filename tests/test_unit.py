
import unittest
from unittest.mock import MagicMock, patch
from main import (
    State,
    LoanApplication,
    update_loan_application_details,
    retrieve_context,
    verify_kyc,
    evaluate_creditworthiness,
    generate_loan_sanction_letter,
)

class TestToolFunctions(unittest.TestCase):
    """Unit tests for the tool functions in main.py."""

    def test_update_loan_application_details(self):
        """
        Tests that the update_loan_application_details function correctly updates the loan application details.
        """
        state = State()
        state = update_loan_application_details(
            state,
            applicant_name="John Doe",
            desired_amount=100000,
            loan_term_months=12,
            purpose="Personal",
        )
        self.assertEqual(state.current_loan_application.applicant_name, "John Doe")
        self.assertEqual(state.current_loan_application.desired_amount, 100000)
        self.assertEqual(state.current_loan_application.loan_term_months, 12)
        self.assertEqual(state.current_loan_application.purpose, "Personal")

    @patch("main.collection")
    def test_retrieve_context(self, mock_collection):
        """
        Tests that the retrieve_context function correctly retrieves context from the ChromaDB collection.
        """
        mock_collection.query.return_value = {
            "documents": [["Test context"]]
        }
        state = State()
        context = retrieve_context(state, query="Test query")
        self.assertEqual(context, "Test context")

    def test_verify_kyc(self):
        """
        Tests that the verify_kyc function correctly verifies the applicant's KYC.
        """
        state = State()
        state.current_loan_application.applicant_name = "John Doe"
        state = verify_kyc(state, "John Doe")
        self.assertTrue(state.current_loan_application.kyc_verified)
        self.assertEqual(state.current_loan_application.status, "credit_check_pending")

    def test_evaluate_creditworthiness(self):
        """
        Tests that the evaluate_creditworthiness function correctly evaluates the applicant's creditworthiness.
        """
        state = State()
        state.current_loan_application.desired_amount = 100000
        state = evaluate_creditworthiness(state, 100000)
        self.assertIn(state.current_loan_application.credit_eligibility, ["eligible", "not_eligible"])

    def test_generate_loan_sanction_letter(self):
        """
        Tests that the generate_loan_sanction_letter function correctly generates a loan sanction letter.
        """
        state = State()
        state.current_loan_application.applicant_name = "John Doe"
        state.current_loan_application.offered_amount = 100000
        state = generate_loan_sanction_letter(state)
        self.assertTrue(state.current_loan_application.sanction_letter_generated)
        self.assertEqual(state.current_loan_application.status, "sanctioned")

if __name__ == "__main__":
    unittest.main()
