import os
from supabase import create_client, Client
from supabase.client import ClientOptions
import logging

from constants.constants import REPO_ANALYSIS_TABLE, TASK_STATUS_PENDING, TASK_TABLE
from models.sqs_queue import SqsQueue


class SupabaseServiceSqs:
    '''
    Service class to interact with Supabase Postgres database. 

    inserts summaries into the repository_analyses table: 
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        repository_id UUID REFERENCES repositories(id) ON DELETE CASCADE,
        created_by UUID REFERENCES profiles(id),  -- Reference to profiles for the user who created the analysis
        summary TEXT,
        title VARCHAR(255),
        username VARCHAR(255),  -- Renamed from user to username
        repo_url TEXT,
        problem_statement TEXT,
        recency_description TEXT,
        demo_description TEXT,
        technologies_description TEXT,
        techniques_description TEXT,
        critics_description TEXT,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()

    insert_repo_analysis: inserts summaries into the repository_analyses table 
    '''

    def __init__(self, secrets_manager):
        self.logger = logging.getLogger(__name__)
        self.secrets_manager = secrets_manager

        self.supabase_client: Client = create_client(
            self.secrets_manager.get("supabase.url"),
            self.secrets_manager.get("supabase.key"),
            options=ClientOptions(
                postgrest_client_timeout=10,
                storage_client_timeout=10,
                schema="public"
            )
        )

    def insert_repo_analysis(self, repository_id: str, created_by: str, summary: str, title: str, username: str, repo_url: str, problem_statement: str, recency_description: str, demo_description: str, technologies_description: str, techniques_description: str, critics_description: str):
        '''
        Inserts a repository analysis into the repository_analyses table
        '''
        try:
            response = self.supabase_client.table(REPO_ANALYSIS_TABLE).insert(
                {
                    "repository_id": repository_id,
                    "created_by": created_by,
                    "summary": summary,
                    "title": title,
                    "username": username,
                    "repo_url": repo_url,
                    "problem_statement": problem_statement,
                    "recency_description": recency_description,
                    "demo_description": demo_description,
                    "technologies_description": technologies_description,
                    "techniques_description": techniques_description,
                    "critics_description": critics_description,
                }
            ).execute()

            # Log the response to understand its structure
            self.logger.info("Insert response: %s", response)

            # Access the data correctly based on the response structure
            if response.data:
                return response.data[0]["id"]
            else:
                self.logger.error("No data in response")
                return None
        except KeyError as e:
            self.logger.error(
                "Extracting id object in insert_repo_analysis: %s", e)
            return None
        except Exception as e:
            self.logger.error("Error in insert_repo_analysis: %s", e)
            return None

    def insert_task(self, task_id: str):
        '''
        Inserts a task into the tasks table
        '''
        try:
            response = self.supabase_client.table(TASK_TABLE).insert(
                {
                    "queue_task_id": task_id,
                    "status": TASK_STATUS_PENDING,
                }
            ).execute()

            # Log the response to understand its structure
            self.logger.info("Insert response: %s", response)

            # Access the data correctly based on the response structure
            if response.data:
                return response.data[0]["id"]
            else:
                self.logger.error("No data in response")
                return None
        except KeyError as e:
            self.logger.error(
                "Extracting id object in insert_task: %s", e)
            raise e
        except Exception as e:
            self.logger.error("Error in insert_task: %s", e)
            raise e

    def insert_task_sqs(self, task_id: str, queue_type=SqsQueue.REPOSITORY):
        '''
        Inserts a task into the tasks table
        Args: 
            task_id (string): The task id to insert
            queue_type (SqsQueue): The type of queue the task is from
        Returns:
            string: The task id
            throws: Exception if there is an error inserting the task
        '''
        try:
            response = self.supabase_client.table(TASK_TABLE).insert(
                {
                    "queue_task_id": task_id,
                    "queue_type": queue_type.name,
                    "status": TASK_STATUS_PENDING,
                }
            ).execute()

            # Log the response to understand its structure
            self.logger.info("Insert response: %s", response)

            # Access the data correctly based on the response structure
            if response.data:
                return response.data[0]["id"]
            else:
                self.logger.error("No data in response")
                return None
        except KeyError as e:
            self.logger.error(
                "Extracting id object in insert_task: %s", e)
            raise e
        except Exception as e:
            self.logger.error("Error in insert_task: %s", e)
            raise e

    def get_task_status(self, task_id: str):
        '''
        Retrieves the status of a task from the tasks table
        '''
        try:
            response = self.supabase_client.table(TASK_TABLE).select(
                "status",
                "message"
            ).eq("queue_task_id", task_id).execute()

            # Log the response to understand its structure
            self.logger.info("Select response: %s", response)

            # Access the data correctly based on the response structure
            if response.data:
                return response.data[0]["status"]
            else:
                self.logger.error("No data in response")
                return "UNKNOWN"
        except KeyError as e:
            self.logger.error(
                "Extracting status object in get_task_status: %s", e)
            raise e
        except Exception as e:
            self.logger.error("Error in get_task_status: %s", e)
            raise e
