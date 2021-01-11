# Verteiler #

### What is this repository for? ###

The repository is used for the "Verteiler"; an application that computes the optimal site-distribution of stationary goods.

### How do I get set up? ###

### 1)  Install Packages:  

        pip install -r requirements.txt

### 2) Authentication (used to Query Google BigQuery):  

If you want your local application to temporarily use your own user credentials for API access, run:
            
        gcloud auth application-default login
    
If you'd like to login by passing in a file containing your own client id, run:

        gcloud auth application-default login  --client-id-file=clientid.json
        
More information on the authentication can be found on https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login