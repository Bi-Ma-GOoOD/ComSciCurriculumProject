import pytest
from unittest.mock import patch, MagicMock
from main.models import Form
from main.services.view_pending_forms_service import ViewPendingFormsService


class TestViewPendingFormsService:
    """Tests for the ViewPendingFormsService class"""

    def setup_method(self):
        """Setup for each test method"""
        # Create a mock user
        self.mock_user = MagicMock()
        self.mock_user.student_code = "12345"
        self.mock_user.name = "John Doe"
        
        # Create mock form - only expecting one based on your error message
        self.mock_form = MagicMock()
        self.mock_form.form_id = "F001"
        self.mock_form.form_type = Form.FormType.GRADUATION_CHECK
        self.mock_form.form_status = Form.FormStatus.PENDING
        self.mock_form.user_fk = self.mock_user
        
        # Setting up a list with one form
        self.mock_forms = [self.mock_form]

    @patch('main.services.view_pending_forms_service.Form.objects.filter')
    def test_get_pending_forms(self, mock_filter):
        """Test that get_pending_forms returns correct data structure"""
        # Set up the mock query to return our mocked forms
        mock_queryset = MagicMock()
        mock_queryset.select_related.return_value = self.mock_forms
        mock_filter.return_value = mock_queryset

        # Call the method under test
        result = ViewPendingFormsService.get_pending_forms()

        # Assert filter was called
        mock_filter.assert_called_once()
        mock_filter.return_value.select_related.assert_called_once_with('user_fk')

        # Verify the result
        assert len(result) == 1
        assert result[0] == {
            'form_id': "F001",
            'form_type': Form.FormType.GRADUATION_CHECK,
            'form_status': Form.FormStatus.PENDING,
            'student_code': "12345",
            'student_name': "John Doe"
        }


    @patch('main.services.view_pending_forms_service.Form.objects.filter')
    def test_get_pending_forms_empty(self, mock_filter):
        """Test that get_pending_forms handles empty queryset correctly"""
        # Set up the mock query to return empty list
        mock_select_related = MagicMock()
        mock_select_related.return_value = []
        mock_filter.return_value = mock_select_related

        # Call the method under test
        result = ViewPendingFormsService.get_pending_forms()

        # Verify the result is empty list
        assert result == []