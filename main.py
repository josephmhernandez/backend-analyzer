from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from constants.constants import ENV_TAVILY_API_KEY, MACHINE_REPO_ID, MACHINE_USER_ID
from models.github_repository_request import GithubRepositoryRequest
import logging
from logging_config import setup_logging
from services.Analyzer import Analyzer
from services.SupabaseService import SupabaseService
from services.GitHubAnalyzer import GitHubAnalyzer
import os
from dotenv import load_dotenv
from services.GitHubHelper import extract_github_info
from utils import helpers
# from services.TavilyService import TavilyService
# Load environment variables
load_dotenv()

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()

github_analyzer = GitHubAnalyzer()  # Instantiate GitHubAnalyzer
# tavily_service = TavilyService()
supabase_service = SupabaseService()


@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"message": "Endpoint doesn't exist"},
    )


@app.get("/")
@app.get("/health")
def read_root():
    return {"message": "Hello World"}


@app.post("/analyze-repository")
async def analyze_repository(input_data: GithubRepositoryRequest):
    try:
        logger.info(
            f"[main] Analyzing repository for: {input_data}")
        # Get the repository data
        username, repository_name = extract_github_info(input_data.repoUrl)

        if not username or not repository_name:
            raise HTTPException(
                status_code=400, detail="Invalid GitHub repository URL")

        an = Analyzer()
        logger.info(
            f"Starting repo AI workflow with username: {username} and repository name: {repository_name}",)
        analysis = an.start_repo_ai_workflow(
            username, repository_name)
        logger.info("Analysis completed")

        # logger.info("Formatting analysis content")
        # for key in analysis:
        #     analysis[key] = helpers.format_analysis_content(analysis[key])

        # Insert the analysis into the database
        logger.info("Inserting analysis into the database")
        res = await supabase_service.insert_repo_analysis(
            input_data.dbRepoId,
            input_data.userId,
            analysis["summary"],
            analysis["title"],
            analysis["user"],  # github username
            analysis["repo_url"],
            analysis["problem_statement"],
            analysis["recency_description"],
            analysis["demo_description"],
            analysis["technologies_description"],
            analysis["techniques_description"],
            analysis["critics_description"],
        )
        logger.info(f"[main] supabase response: {res}")
        logger.info("[main] Analysis inserted into the database")
        # return {"result": analysis}
    except Exception as ex:
        logger.error(f"[main] Error analyzing repository: {str(ex)}")
        # insert error into the database
        try:  # Insert the error into the database
            res = await supabase_service.insert_repo_analysis(
                input_data.dbRepoId,
                input_data.userId,
                "Error creating analysis. We're looking into it.",
                input_data.repoName,
                "",
                input_data.repoUrl,
                "",
                "",
                "",
                "",
                "",
                "",
            )
        except Exception as db_insert_error:
            logger.error(
                f"[main] Error inserting error into the database: {str(db_insert_error)}")
            raise HTTPException(
                status_code=500, detail="Error in analysis and error inserting into the database")

        logger.error(
            f"Error Analyzing this repository. Error inputted into analysis DB table: {input_data.dbRepoId}")

        raise HTTPException(status_code=400, detail=str(ex))


@app.post("/input-data-local")
async def input_data(input_data: dict):

    repo_id = input_data.get("repo_id")
    user_id = input_data.get("user_id")
    if not repo_id or not user_id:
        return {"error": "repo_id and user_id are required"}

    input_data = {
        "recency_description": "This project was started on August 4th, 2022 and the last commit was made on February 1st, 2024. This project is a web application for ordering custom maps. The project's history is filled with features related to map customization, ordering, and checkout.  Some of the key features include:\n\n* **Map Customization:**  The project focuses on providing users with tools to customize maps, including adding pins, text, and other visual elements.\n\n* **Ordering:**  Users can order their customized maps through a well-defined checkout process.\n\n* **Mobile Optimization:**  The project has been optimized for mobile devices, ensuring a responsive user experience across various screen sizes.\n\n* **User Experience:**  The commit history indicates significant attention to user experience, focusing on refining the visual design, layout, and interactions to enhance usability.\n\n* **Google Analytics:**  The integration of Google Analytics allows the developers to track user behavior and website performance.\n\n* **Email Automation:**  The system seems to include email automation capabilities for sending order confirmations, special requests, and other relevant communications.\n\n* **Stripe Payment Integration:**  The project integrates with Stripe to process payments securely.\n\n* **Database Integration:**  A database is used to store user data, order information, and reviews.\n\n* **Accordion and Carousel Elements:**  The project utilizes accordion and carousel elements for enhancing user interactions and presenting information in a visually appealing manner.\n\n* **Tailored Requests:**  A special request feature allows users to customize their maps with more personalized requirements.\n\n* **Gallery Browse:**  The project includes a gallery browse feature, potentially for showcasing examples of custom maps.\n\n* **Tailwind CSS:**  The commit history shows a shift to using Tailwind CSS for styling, indicating a move towards a more modern and responsive design approach.\n\n* **Offer Modal:**  The application features an offer modal for showcasing promotions and special offers.\n\n* **Product Descriptions:**  The project incorporates product descriptions to provide detailed information about the available map options.\n\n* **Pinterest Integration:**  The project utilizes Pinterest tags for enhancing website discoverability and social media marketing.\n\nThe project's ongoing development suggests a commitment to providing users with a high-quality, feature-rich, and customizable experience for creating and ordering their personalized maps.",
        "technologies_description": "This project utilizes a range of technologies to deliver a robust web application.  The front-end is built with Next.js, a React framework, leveraging its server-side rendering capabilities and optimized performance. For styling, the project utilizes Chakra UI for its component library and Tailwind CSS for a utility-first approach to styling.  \n\nThe project utilizes a combination of React libraries for various functionalities, including:\n\n* **React Hook Form** for streamlined form management\n* **React Router DOM** for client-side routing\n* **React Leaflet** for map integration\n* **Redux and Redux Toolkit** for state management\n* **React-toastify** for user notifications\n\nFor data fetching and interactions, the project uses Axios for HTTP requests. \n\nOn the back-end, the project integrates with AWS services, leveraging:\n\n* **AWS Amplify** for authentication and backend infrastructure management.\n* **AWS DynamoDB** as a NoSQL database.\n* **AWS SDK** for interactions with AWS services.\n\nThe project also incorporates other libraries for various purposes:\n\n* **Lottie-react** for animations.\n* **Rudder SDK** for analytics tracking.\n* **SendGrid** for email communication.\n* **Stripe** for payment processing.\n\nOverall, this project demonstrates a modern web development approach, combining powerful frameworks with AWS services for a scalable and feature-rich application.",
        "summary": "The project is a web application for selling custom maps, built with Next.js, React, and AWS services. It provides a user-friendly platform for designing, visualizing, and purchasing personalized maps. While the project implements several core features and utilizes a modern technology stack, there are areas for improvement in terms of efficiency and coding practices, particularly in the `pages/index.js`, `store/index.js`, and `components/layout/Layout.js` files.  These files exhibit issues like redundant image fetching, inconsistent styling, lack of error handling, and minimal use of Redux capabilities.  By addressing these concerns, the project can be optimized for performance, maintainability, and better code readability.",
        "problem_statement": "This project is designed for a business selling custom maps, solving the problem of providing an accessible and user-friendly platform for customers to design and purchase personalized maps. The target audience is individuals or businesses seeking unique and memorable gifts, home decor, or promotional materials.\n\nThe project aims to streamline the process of creating and ordering custom maps, offering a platform that:\n\n* **Simplifies map customization:** Users can easily select map styles, customize colors, add pins, and adjust the size and dimensions of their maps.\n* **Provides visual representation:** A map preview is displayed in real-time, allowing users to visualize their customized map before ordering.\n* **Offers seamless checkout:** A streamlined checkout process allows users to securely enter payment details and complete their purchase.\n* **Delivers high-quality products:** The platform ensures that the final maps are printed with high quality and delivered to the customer promptly.",
        "critics_description": "The analysis of the important files identified several areas for improvement in terms of efficiency and coding practices.  \n\n**Pages/index.js**\n\n* **Redundant Image Fetching:** Fetch images once and use conditional rendering for mobile and desktop views.\n* **Unnecessary State Updates:** Use single values instead of arrays for state updates.\n* **Inconsistent Styling:** Adopt a consistent approach to styling using either inline styles or Tailwind CSS classes.\n* **Performance Improvements:** Optimize image loading and CSS for faster rendering.\n* **Missing Error Handling:** Implement error handling for image fetching and display feedback to the user.\n* **Unnecessary `useEffect` Dependency:** Remove the dependency on an empty array for cleaner code.\n* **Inconsistent Naming Conventions:** Use consistent naming conventions for variables and components.\n* **Unnecessary Comments:** Remove comments that don't provide value.\n* **Hardcoded Values:** Refactor image paths and sizes into constants for better maintainability.\n* **Lack of Unit Tests:** Add unit tests to ensure component functionality and prevent regressions.\n\n**Store/index.js**\n\n* **Minimal Configuration:** Enhance the store's functionality by adding options like middleware.\n* **Lack of Thunks or Sagas:** Implement Redux Thunks or Sagas for handling asynchronous operations.\n* **Potential for Redundant Actions:**  Organize the store into multiple slices for better modularity if the application grows in complexity.\n* **Limited Error Handling:** Add error handling mechanisms for state updates and asynchronous actions.\n* **Missing Unit Tests:** Add unit tests for state updates and actions.\n\n**Components/layout/Layout.js**\n\n* **Modularization:** Extract the header and footer components into separate files for better organization and reusability.\n* **Conditional Rendering:**  Implement conditional rendering for the header and footer components based on user authentication or page context.\n* **Context API:**  Utilize the React Context API to share data and functionality with child components.\n* **Use of Props:**  Accept props for customization, like page title or header/footer content, to enhance flexibility.\n* **Dynamic Styling:** Use CSS modules or dynamic styling techniques for better styling flexibility and maintainability.",
        "techniques_description": "The project utilizes a combination of technologies and software engineering techniques to create a user-friendly and feature-rich platform for designing and purchasing custom maps, catering to the specific needs of the map customization industry.\n\nThe project leverages a blend of front-end and back-end technologies to create a robust and engaging user experience. The front-end is powered by Next.js, a React framework known for its server-side rendering capabilities and performance optimizations. The project utilizes Chakra UI for its comprehensive component library and Tailwind CSS for its utility-first approach to styling.\n\nThe project incorporates a range of React libraries for functionalities such as:\n\n* **React Hook Form:** For streamlined form management.\n* **React Router DOM:** For client-side routing.\n* **React Leaflet:** For integrating interactive maps.\n* **Redux and Redux Toolkit:** For managing application state.\n* **React-toastify:** For displaying user notifications.\n\nFor data fetching and interactions, the project utilizes Axios for HTTP requests.\n\nOn the back-end, the project integrates with AWS services, leveraging:\n\n* **AWS Amplify:** For authentication, backend infrastructure management, and hosting.\n* **AWS DynamoDB:** As a NoSQL database for storing user data, orders, and reviews.\n* **AWS SDK:** For interactions with AWS services.\n\nAdditionally, the project incorporates libraries for:\n\n* **Lottie-react:** For animations.\n* **SendGrid:** For email communication.\n* **Stripe:** For payment processing.\n\nThe project employs several software engineering techniques for efficiency, scalability, and maintainability. These include:\n\n* **Server-side rendering (SSR) with Next.js:**  Enhancing SEO and initial page load speed.\n* **State management with Redux Toolkit:**  Ensuring a predictable and manageable application state.\n* **Component-based architecture with React:**  Breaking down the UI into reusable components for easier development and maintenance.\n* **API integration with AWS services:**  Leveraging cloud services for scalability, authentication, and data storage.\n* **Responsive design:** Adapting the user interface to various screen sizes for optimal mobile and desktop experiences.\n* **Testing and debugging:** Implementing tests to ensure code functionality and using debugging tools to identify and resolve issues.\n* **Continuous integration and deployment (CI/CD) with AWS Amplify:**  Automating the build, test, and deployment processes for seamless updates.",
        "repo_url": "https://github.com/josephmhernandez/lyfe-captures",
        "user": "josephmhernandez",
        "title": "lyfe-captures",
        "created_at": "2024-08-19 11:56:47+0000",
        "demo_description": ""
    }
    res = await supabase_service.insert_repo_analysis(
        repository_id=repo_id,
        created_by=user_id,
        summary=input_data["summary"],
        title=input_data["title"],
        username=input_data["user"],
        repo_url=input_data["repo_url"],
        problem_statement=input_data["problem_statement"],
        recency_description=input_data["recency_description"],
        demo_description=input_data["demo_description"],
        technologies_description=input_data["technologies_description"],
        techniques_description=input_data["techniques_description"],
        critics_description=input_data["critics_description"],
    )
    print(res)
    return {"result": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
