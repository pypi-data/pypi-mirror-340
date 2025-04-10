# textops/api.py

import requests
import json
import time
from typing import Dict, Any, Optional, Union


class TextOpsAPI:
    """Client for interacting with TextOps transcription API"""
    
    BASE_URL = "https://text-ops-subs.com/api/v1"
    
    def __init__(self, api_key: str):
        """
        Initialize TextOps API client
        
        Args:
            api_key: Your TextOps API key
        """
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'textops-api-key': api_key,
            'Accept': 'application/json'
        }
    
    def submit_transcription(self, audio_url: str) -> Dict[str, Any]:
        """
        Submit audio for transcription
        
        Args:
            audio_url: URL to the audio file to be transcribed
            
        Returns:
            API response containing job ID and status information
            
        Raises:
            requests.exceptions.RequestException: If API request fails
        """
        data = {
            'audio': audio_url
        }
        
        response = requests.post(
            f"{self.BASE_URL}/submit", 
            headers=self.headers, 
            data=json.dumps(data)
        )
        
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    
    def check_status(self, job_id: str) -> Dict[str, Any]:
        """
        Check transcription job status once
        
        Args:
            job_id: The job identifier returned by submit_transcription
            
        Returns:
            Status response from API
            
        Raises:
            requests.exceptions.RequestException: If API request fails
        """
        job = {'textopsJobId': job_id}
        
        response = requests.post(
            f"{self.BASE_URL}/status",
            headers=self.headers,
            data=json.dumps(job)
        )
        
        return response.json()
    
    def wait_for_completion(
        self, 
        job_id: str, 
        max_attempts: int = 15, 
        wait_seconds: int = 20
    ) -> Optional[Dict[str, Any]]:
        """
        Repeatedly check job status until text is available or an error occurs
        
        Args:
            job_id: The job identifier returned by submit_transcription
            max_attempts: Maximum number of status check attempts (default: 15)
            wait_seconds: Wait time between attempts in seconds (default: 20)
            
        Returns:
            Final API response with transcription text or error information,
            or None if max attempts reached without completion
        """
        attempts = 0
        
        while attempts < max_attempts:
            attempts += 1
            
            try:
                result = self.check_status(job_id)
                
                # Return if text is available
                if 'text' in result and result['text'] is not None:
                    return result
                
                # Return if error occurred
                if 'has_error' in result and result['has_error'] is True:
                    return result
                
                # Wait before next attempt
                time.sleep(wait_seconds)
                
            except Exception as e:
                if attempts < max_attempts:
                    time.sleep(wait_seconds)
                else:
                    raise e
        
        return None
    
    def transcribe(
        self, 
        audio_url: str, 
        max_attempts: int = 15, 
        wait_seconds: int = 20
    ) -> Dict[str, Any]:
        """
        Submit audio for transcription and wait for completion
        
        Args:
            audio_url: URL to the audio file to be transcribed
            max_attempts: Maximum number of status check attempts (default: 15)
            wait_seconds: Wait time between attempts in seconds (default: 20)
            
        Returns:
            Final result with transcription text or error information
            
        Raises:
            ValueError: If transcription failed or timed out
        """
        # Submit for transcription
        submission = self.submit_transcription(audio_url)
        job_id = submission.get('textopsJobId')
        
        if not job_id:
            raise ValueError(f"Failed to get job ID: {submission}")
        
        # Wait for completion
        result = self.wait_for_completion(job_id, max_attempts, wait_seconds)
        
        if not result:
            raise ValueError(f"Transcription timed out after {max_attempts} attempts")
            
        if 'has_error' in result and result['has_error'] is True:
            error_msg = result.get('message', 'Unknown error')
            raise ValueError(f"Transcription failed: {error_msg}")
            
        return result