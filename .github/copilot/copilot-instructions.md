# GitHub Copilot Instructions

This is a social network application built with Django (backend) and Vue.js (frontend). When providing suggestions, please consider the following context:

## Project Structure
- `backend/`: Django REST API
  - `account/`: User authentication and profile management
  - `chat/`: Real-time messaging system
  - `notification/`: User notifications
  - `post/`: Social media posts and interactions
  - `search/`: Search functionality
- `frontend/`: Vue.js application
  - Uses TypeScript, Tailwind CSS, and Vue Router
  - Firebase integration for additional features

## Code Style Guidelines
- Backend (Python):
  - Follow PEP 8 style guide
  - Use Django REST framework conventions
  - Include docstrings for classes and methods
  - Type hints are encouraged

- Frontend (TypeScript/Vue):
  - Use Composition API with `<script setup lang="ts">`
  - Follow Vue.js Style Guide priorities A and B
  - Strong typing with TypeScript interfaces
  - Use Tailwind CSS for styling

## Key Features to Consider
- User authentication and authorization
- Real-time chat functionality
- Social interactions (posts, likes, comments)
- Friend requests and connections
- Notifications system
- Search capabilities
- Media handling (avatars, post attachments)

## Important Patterns
- Use Django serializers for API responses
- Implement proper API error handling
- Follow RESTful API design principles
- Vue components should be single-responsibility
- State management using Pinia
- TypeScript interfaces for API responses

When suggesting code:
1. Maintain consistency with existing patterns
2. Consider security implications
3. Follow established naming conventions
4. Include necessary imports
5. Add appropriate error handling
6. Consider performance implications