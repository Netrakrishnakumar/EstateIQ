# Estate IQ - Smart House Price Prediction

A modern web application that leverages IBM Watson Studio AutoAI to provide accurate house price predictions. Built with Python Flask for the backend and Bootstrap 5 for a responsive, professional frontend.

## Features

- **AI-Powered Predictions**: Uses IBM Watson Studio AutoAI for accurate property price estimation
- **Responsive Design**: Clean, professional UI that works on all devices
- **Easy Integration**: Simple setup with IBM Cloud credentials
- **Real-time Results**: Get instant predictions through REST API calls
- **User-Friendly**: Intuitive form with validation and error handling

## Technologies Used

### Backend
- Python Flask - Web framework
- IBM Cloud SDK - Cloud integration
- Requests - HTTP library
- Python-dotenv - Environment management

### Frontend
- HTML5 - Markup
- Bootstrap 5 - UI framework
- CSS3 - Styling
- JavaScript - Interactivity

## Prerequisites

- Python 3.8 or higher
- IBM Cloud account with Watson Studio
- Deployed AutoAI model for house price prediction
- IBM Cloud API Key
- Watson Studio deployment URL

## Installation

1. **Clone or download the project**

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix/MacOS:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure IBM Cloud credentials**

   Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

   Edit `.env` and add your IBM Cloud credentials:
   ```
   IBM_API_KEY=your_ibm_cloud_api_key_here
   IBM_DEPLOYMENT_URL=your_watson_studio_deployment_url_here
   IBM_SPACE_ID=your_watson_studio_space_id_here
   IBM_REGION=your_ibm_cloud_region_here
   ```

### Getting IBM Cloud Credentials

1. **IBM API Key**:
   - Go to [IBM Cloud Console](https://cloud.ibm.com/)
   - Navigate to Manage > Access (IAM) > API Keys
   - Create a new API key and copy it

2. **Deployment URL**:
   - Go to IBM Watson Studio
   - Navigate to your deployed AutoAI model
   - Copy the deployment endpoint URL

3. **Space ID**:
   - In Watson Studio, go to your deployment space
   - The Space ID is available in the space details

4. **Region**:
   - Your IBM Cloud region (e.g., `us-south`, `eu-de`, `jp-tok`)

## Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open your browser**
   Navigate to: `http://localhost:5000`

## Project Structure

```
Estate-IQ/
├── app.py                 # Flask application with API endpoints
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .env.example          # Environment variables template
├── .env                  # Your actual credentials (create this)
├── templates/
│   ├── index.html        # Home page
│   ├── predict.html      # Prediction form page
│   └── about.html        # About page
├── static/
│   ├── style.css         # Custom styles
│   └── script.js         # Frontend JavaScript
└── utils/
    └── ibm_client.py     # IBM Cloud integration module
```

## API Endpoints

### POST /api/predict
Submit property details for price prediction.

**Request Body:**
```json
{
  "Area": 1500,
  "Bedrooms": 3,
  "Bathrooms": 2,
  "Garage": 2,
  "Floors": 2,
  "Condition": "Excellent",
  "YearBuilt": 2020,
  "Location": "downtown"
}
```

**Response:**
```json
{
  "success": true,
  "prediction": 250000,
  "currency": "USD"
}
```

### GET /health
Health check endpoint to verify the application status.

## Customization

### Modifying Input Fields

The prediction form fields can be modified in two places:

1. **Frontend** (`templates/predict.html`):
   - Add or remove form fields in the HTML form

2. **Backend** (`app.py`):
   - Update the `required_fields` list in the `/api/predict` endpoint
   - Update the `processed_data` dictionary to match your model's features

### Adjusting Model Features

If your IBM Watson Studio AutoAI model uses different features:

1. Update the form fields in `templates/predict.html`
2. Modify the `required_fields` list in `app.py`
3. Update the data processing logic in the `/api/predict` endpoint
4. Adjust the field names in `static/script.js` if needed

## Troubleshooting

### Common Issues

1. **"IBM Cloud client not initialized"**
   - Check that your `.env` file exists and contains valid credentials
   - Verify all four environment variables are set

2. **"Failed to generate IAM token"**
   - Verify your IBM API Key is correct
   - Check that your API Key has the necessary permissions

3. **"Failed to call deployment endpoint"**
   - Verify the deployment URL is correct
   - Check that your deployment is active in Watson Studio
   - Ensure the region matches your deployment location

4. **Prediction returns unexpected values**
   - Verify the input fields match your model's expected features
   - Check the data types (numeric vs string) match your model's requirements

## Security Notes

- Never commit `.env` file to version control
- Keep your IBM Cloud API Key secure
- Use environment variables for all sensitive credentials
- Consider using IBM Cloud Secrets Manager for production deployments

## License

This project is created for educational purposes as part of an IBM Internship Final Project.

## Support

For issues related to:
- **IBM Cloud/Watson Studio**: Visit [IBM Cloud Documentation](https://cloud.ibm.com/docs)
- **Flask**: Visit [Flask Documentation](https://flask.palletsprojects.com/)
- **Bootstrap**: Visit [Bootstrap Documentation](https://getbootstrap.com/docs/)

## Acknowledgments

- IBM Watson Studio AutoAI for providing the machine learning platform
- Bootstrap team for the excellent UI framework
- Flask community for the robust web framework
