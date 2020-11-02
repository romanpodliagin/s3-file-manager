# Docker
     # Set Env
     * cp envs/.env.template s3_file_manager/.env
     * SET:
        * AWS_ACCESS_KEY_ID
        * AWS_SECRET_ACCESS_KEY
        * AWS_STORAGE_BUCKET_NAME
        
     * docker-compose up --build
 
# Manually 
    # Install
     * install venv with python3.8
     * python -m pip install -r requirements.txt

    # Set Env
     * cp envs/.env.template s3_file_manager/.env
     * SET:
        * AWS_ACCESS_KEY_ID
        * AWS_SECRET_ACCESS_KEY
        * AWS_STORAGE_BUCKET_NAME
         
    # Load Models
     * python manage.py migrate
     * python manage.py load_models
     
    # Run Server
     * python manage.py runserver