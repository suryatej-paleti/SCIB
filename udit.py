import requests
from typing import Type
from pydantic import BaseModel, Field, constr
from crewai.tools import BaseTool


# =========================================================
# INPUT SCHEMA
# ONLY BEARER TOKEN IS USER INPUT
# =========================================================
class ExecutePipelineSchema(BaseModel):
    bearer_token: constr(
        min_length=1,
        max_length=3000
    ) = Field(
        ...,
        description="Bearer access token (runtime input only)"
    )


# =========================================================
# CREWAI TOOL
# =========================================================
class ExecutePipelineTool(BaseTool):
    """
    Triggers workflow execution using multipart/form-data
    EXACTLY matching the working curl.
    """

    name: str = "AAVA_Pipeline_Executor_Bearer"
    description: str = "Executes AAVA workflow with fixed URL and Bearer token authentication."
    args_schema: Type[BaseModel] = ExecutePipelineSchema

    # ===== FIXED VALUES (FROM CURL) =====
    fixed_pipeline_api_url: str = "https://aava-int.avateam.io/workflows/workflow-executions"
    fixed_pipeline_id: str = "8124"
    fixed_user_email: str = "keerthana.pyarasani@ascendion.com"
    fixed_user_inputs: str = (
        '{"{{user input_string_true_user%252520request}}":".",'
        '"{{pipeline_api_false_string}}":".",'
        '"{{access_key_false_true}}":"."}'
    )
    fixed_priority: str = "1"
    fixed_realm_id: str = "32"

    def _run(self, bearer_token: str) -> str:
        try:
            headers = {
                "accept": "application/json, text/plain, */*",
                "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
                "authorization": f"Bearer {bearer_token}",
                "origin": "https://aava-int.avateam.io",
                "referer": "https://aava-int.avateam.io/launchpad/build/workflows/playground?id=8124",
                "x-realm-id": self.fixed_realm_id,
                "user-agent": "Mozilla/5.0 (CrewAI)"
            }

            files = {
                "pipelineId": (None, self.fixed_pipeline_id),
                "user": (None, self.fixed_user_email),
                "userInputs": (None, self.fixed_user_inputs),
                "priority": (None, self.fixed_priority)
            }

            response = requests.post(
                self.fixed_pipeline_api_url,
                headers=headers,
                files=files,
                timeout=60
            )

            if response.ok:
                return (
                    "✅ Workflow triggered successfully\n"
                    f"Pipeline ID: {self.fixed_pipeline_id}\n"
                    f"Status Code: {response.status_code}\n"
                    f"Response: {response.text}"
                )

            return (
                "❌ Workflow trigger failed\n"
                f"Pipeline ID: {self.fixed_pipeline_id}\n"
                f"Status Code: {response.status_code}\n"
                f"Error: {response.text}"
            )

        except Exception as e:
            return f"❌ Exception occurred: {str(e)}"


# =========================================================
# LOCAL / AGENT EXECUTION
# =========================================================
if __name__ == "__main__":
    tool = ExecutePipelineTool()

    result = tool._run(
        bearer_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJXaWh1aHM1U1JPZHZtNzV6Rk1PdEt2UlQtMjRDTFJPSlE5ZzlMQnQ3SHlrIiwiaWF0IjoxNzY4NTQ0NjczLCJleHAiOjE3Njg1NDk5NDUsImF1ZCI6IjAwMDAwMDAzLTAwMDAtMDAwMC1jMDAwLTAwMDAwMDAwMDAwMCIsInRpZCI6ImQ3NzU4ZThmLTFkZjMtNDg5Zi04NmI1LWEyMjU0ZjU1ZjljYyIsImFwcGlkIjoiY2U2Y2M0MjEtYmZjZi00ZGI3LTg3MGEtOTA0ZTc4OGFkYThmIiwidW5pcXVlX25hbWUiOiJrZWVydGhhbmEucHlhcmFzYW5pQGFzY2VuZGlvbi5jb20iLCJkb21haW4iOiJhYXZhLWludC5hdmF0ZWFtLmlvIiwidXNlckRldGFpbHMiOiJTbHh2OUVpMEl1N29YbjhSdDJxaFg1T1pIQW0ybzFkSDRnaEI5ZkdzS3lkR3lEK3lqd0tTMjN4OXgrS243TUQ3dkx3YkhaTmM4L3pLNmpXTlovNlQ0cDVsUlJpQ0o5dlg5V2NqWGJ2L1JBclIrTjV0bjRJS1BUemxMNmNraGZPOXVZOTgzd3craVAyRHZkcmhWSFpSdVljdy9Oa0lVLzFVdnhITnZJZmdOZms2T1ZEa1FvT1RTcG5RSEZJRHJEdHFnWFdBZmpnTysxV1FhWEpOa3FCOHNMUTNQaDRVWVdWUkdKaTBWcG81a0I2ZGlGMjFOeFdvaFNlT0RQUkhuZm1CR1lsU2ZRdVg4dmVoekEzYzk1SUUrdz09In0.BF_BNyhufurxHkjznlyAFYqP_U7TkbVr6EvzHP9xZyOML93vGyDK-td9iPVATwF0KwmyCySjX9vBazFqJCpQt-gtKUeBKk164uApIFvbcymZli9G6erM3WBT75FBj2AqG8f9tWVEPJG47lp0_RxaVJ3v1ZFdVhz-8IPG_PojuQ5qPNl7uylg33A4aL9fjdPgCBO1HqqSWQbQcGDcunnSQv0wqn7araezQ0zq3KYVbbXPYUMo1M05EF8ymSrMx7dZy6qB32qHr3UcGTfl47zJrOes3uL6v9sG4E2Cr0-K14CWUdlyRgGAc_MyfAMyUOlvOomNOyAtKYuhOE6qZfS-Xw"
    )

    print(result)
    
 