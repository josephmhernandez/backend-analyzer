import os
from supabase import create_client, Client
from supabase.client import ClientOptions
import logging

from constants.constants import REPO_ANALYSIS_TABLE


class SupabaseService:
    '''
    Service class to interact with Supabase Postgres database. 

    inserts summaries into the repository_analysesn table: 
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

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.supabase_client: Client = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY"),
            options=ClientOptions(
                postgrest_client_timeout=10,
                storage_client_timeout=10,
                schema="public"
            )
        )

    async def insert_repo_analysis(self, repository_id: str, created_by: str, summary: str, title: str, username: str, repo_url: str, problem_statement: str, recency_description: str, demo_description: str, technologies_description: str, techniques_description: str, critics_description: str):
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
