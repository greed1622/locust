from locust import HttpUser, task, between

class LaravelUser(HttpUser):
    wait_time = between(1, 3)
    token = None

    def on_start(self):
        # Step 1: Get the CSRF token
        response = self.client.get("/login", verify=False)  # Disable SSL verification
        csrf_token = self.get_csrf_token(response.text)

        # Step 2: Use the CSRF token in the login request
        login_payload = {
            "email": "pingzr022@gmail.com",
            "password": "51622313",
            "_token": csrf_token  # CSRF token included here
        }

        # Step 3: Send the login request with CSRF token
        response = self.client.post("/login", data=login_payload, verify=False)  # Disable SSL verification

        # Check if login was successful (optional)
        if response.status_code == 200:
            print("Login successful")
        else:
            print(f"Login failed with status: {response.status_code}")

    def get_csrf_token(self, response_text):
        """Extract the CSRF token from the HTML response."""
        import re
        match = re.search(r'\'csrf-token\' content="(.+?)"', response_text)
        if match:
            return match.group(1)
        else:
            return None

    @task
    def load_dashboard(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/list-of-patients", headers=headers, verify=False)  # Disable SSL verification

    @task
    def load_patient_details(self):
        headers ={"Authorization": f"Bearer {self.token}"}
        self.client.get("patient-details/3",headers=headers, verify=False)
    
    @task
    def view_schedule(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/patient/view-schedule", headers=headers, verify=False)