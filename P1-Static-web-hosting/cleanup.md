\# Cleanup Guide



\## AWS Resources Used



This project used Amazon S3 for static website hosting and Amazon Route 53 for DNS routing.



\## Cleanup Steps



Since the AWS resources have already been deleted, no further cleanup is required.



If deploying this project again, remember to:



1\. Remove the Route 53 DNS records created specifically for this project, if they are no longer needed.

2\. Delete the S3 bucket after removing its objects and any required versions.

3\. Check for any remaining AWS resources associated with the project.

4\. Review AWS Billing to confirm that no unexpected charges remain.



\*\*Important:\*\* Do not delete shared DNS records or resources used by other projects.



