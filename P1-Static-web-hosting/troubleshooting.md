\# Troubleshooting Guide



\## 1. Website Is Not Loading



\- Verify that the S3 bucket was configured for static website hosting.

\- Confirm that the website files, including `index.html`, were uploaded.

\- Check the S3 bucket policy and permissions.



\## 2. Access Denied Error



\- Review the bucket policy and confirm that the required permissions are correct.

\- Check whether S3 Block Public Access settings conflict with the intended hosting configuration.

\- Never make a bucket public if it contains private or sensitive data.



\## 3. Custom Domain Is Not Working



\- Verify that the Route 53 hosted zone contains the correct DNS records.

\- Confirm that the records point to the intended website endpoint.

\- Allow time for DNS changes to propagate.



\## 4. Website Shows an Old Version



\- Clear the browser cache and reload the page.

\- If a CDN was configured, check its cache settings.



\## Note



The AWS resources for this project have been deleted, so these steps are provided as troubleshooting guidance for a future deployment.



