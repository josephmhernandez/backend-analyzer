# import pytest
# import sys

# from services.Analyzer import Analyzer


# def test_extract_json_from_text_returns_correct_values():
#     text = """{
#         "technologies_description": "This project utilizes a combination of technologies, including:\\n\\n**Frontend:**\\n* **Next.js:** A React framework for building server-side rendered and static websites and web applications.\\n* **React:** A JavaScript library for building user interfaces.\\n* **Chakra UI:** A component library for building accessible and modular user interfaces.\\n* **Mantine:** A React component library focused on accessibility and responsiveness.\\n* **Material UI:** A component library based on Google's Material Design.\\n* **React Router DOM:** A library for managing navigation in React applications.\\n* **Redux:** A predictable state container for JavaScript apps.\\n* **Redux Toolkit:** A set of tools for simplifying Redux development.\\n* **SWR:** A React hook for data fetching and caching.\\n* **Flowbite:** A set of responsive UI components built with Tailwind CSS.\\n* **Flowbite React:** React component library for Flowbite components.\\n* **Leaflet:** A JavaScript library for interactive maps.\\n* **React Leaflet:** A wrapper library for Leaflet for use with React.\\n* **Lottie React:** A library for rendering Lottie animations in React applications.\\n* **React Hook Form:** A library for building forms in React applications.\\n* **React Toastify:** A library for displaying notifications in React applications.\\n\\n**Backend:**\\n* **AWS Amplify:** A serverless framework for building and deploying web and mobile applications on AWS.\\n* **AWS SDK for JavaScript:** A client library for interacting with AWS services.\\n* **Amazon DynamoDB:** A fully managed NoSQL database service.\\n* **SendGrid:** A cloud-based email service.\\n* **Stripe:** A payment processing platform.\\n* **Axios:** A promise-based HTTP client.\\n\\n**Other:**\\n* **Tailwind CSS:** A utility-first CSS framework.\\n* **PostCSS:** A tool for transforming stylesheets.\\n* **Autoprefixer:** A tool for adding vendor prefixes to CSS.\\n* **ESLint:** A JavaScript linter.\\n* **dotenv:** A library for loading environment variables from a .env file."
#         }"""
#     analyzer = Analyzer()
#     extracted_json = analyzer.extract_json_from_text(text)

#     expected_json = ""
#     assert extracted_json == expected_json
