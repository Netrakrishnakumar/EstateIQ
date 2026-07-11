"""
Estate IQ - Smart House Price Prediction
Flask Backend Application
Integrates with IBM Watson Studio AutoAI Deployment
"""

import os
import logging
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from utils.ibm_client import IBMCloudClient

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize IBM Cloud Client
ibm_client = None


def init_ibm_client():
    """Initialize IBM Cloud client with environment variables"""
    global ibm_client
    
    api_key = os.getenv('IBM_API_KEY')
    deployment_url = os.getenv('IBM_DEPLOYMENT_URL')
    space_id = os.getenv('IBM_SPACE_ID')
    region = os.getenv('IBM_REGION')
    
    if not all([api_key, deployment_url, space_id, region]):
        logger.error("Missing IBM Cloud credentials in environment variables")
        return False
    
    try:
        ibm_client = IBMCloudClient(api_key, deployment_url, space_id, region)
        logger.info("IBM Cloud client initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize IBM Cloud client: {str(e)}")
        return False


# Initialize IBM client on startup
init_ibm_client()


@app.route('/')
def home():
    """Render home page"""
    return render_template('index.html')


@app.route('/predict')
def predict():
    """Render prediction page"""
    return render_template('predict.html')


@app.route('/about')
def about():
    """Render about page"""
    return render_template('about.html')


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """
    API endpoint for house price prediction
    Expects JSON with property features
    Returns prediction result
    """
    try:
        # Check if IBM client is initialized
        if not ibm_client:
            return jsonify({
                'success': False,
                'error': 'IBM Cloud client not initialized. Please check your credentials.'
            }), 500
        
        # Get input data from request
        input_data = request.get_json()
        
        if not input_data:
            return jsonify({
                'success': False,
                'error': 'No input data provided'
            }), 400
        
        # Validate required fields (adjust based on your model)
        required_fields = [
    'Id',
    'Area',
    'Bedrooms',
    'Bathrooms',
    'Floors',
    'YearBuilt',
    'Location',
    'Condition',
    'Garage'
]
        
        missing_fields = [field for field in required_fields if field not in input_data]
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Convert string values to appropriate types
        try:
            processed_data = {
    'Id': int(input_data['Id']),
    'Area': float(input_data['Area']),
    'Bedrooms': int(input_data['Bedrooms']),
    'Bathrooms': int(input_data['Bathrooms']),
    'Floors': int(input_data['Floors']),
    'YearBuilt': int(input_data['YearBuilt']),
    'Location': str(input_data['Location']),
    'Condition': str(input_data['Condition']),
    'Garage': str(input_data['Garage'])
}
        except (ValueError, TypeError) as e:
            return jsonify({
                'success': False,
                'error': f'Invalid data type: {str(e)}'
            }), 400
        
        # Call IBM Watson Studio deployment
        logger.info("Processing prediction request...")
        prediction_result = ibm_client.predict(processed_data)
        
        if not prediction_result:
            return jsonify({
                'success': False,
                'error': 'Failed to get prediction from IBM Watson Studio'
            }), 500
        
        # Extract prediction value
        predicted_value = ibm_client.get_prediction_value(prediction_result)
        
        if predicted_value is None:
            return jsonify({
                'success': False,
                'error': 'Failed to extract prediction value from response'
            }), 500
        
        logger.info(f"Prediction successful: {predicted_value}")
        
        return jsonify({
            'success': True,
            'prediction': predicted_value,
            'currency': 'USD'  # Adjust based on your model's currency
        })
        
    except Exception as e:
        logger.error(f"Unexpected error in prediction: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'ibm_client_initialized': ibm_client is not None
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
