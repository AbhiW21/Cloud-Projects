# Static website hosting using Amazon S3 + Route 53.

<img width="858" height="387" alt="image" src="https://github.com/user-attachments/assets/fc10b177-205f-4939-8861-2653e748a26d" />

## Step #1: Set Up Amazon S3 Bucket
- Go to the AWS Management Console and open the Amazon S3 console.
- Click "Create bucket" and enter a unique name for your bucket.
- In the "Properties" section, enable "Static website hosting."
- Upload your website files to the bucket.
- Set the bucket permissions to allow public access.

## Step #2: Purchase a Custom Domain through Amazon Route 53
- Open the Amazon Route 53 console.
- Choose "Domain registration" and then "Register domain."
- Follow the prompts to purchase your custom domain.
- In the "Route 53 hosted zones," create a new record set.
- Enter your S3 bucket's endpoint as the alias target.

## Step #3: (If needed) You can also setup CloudFront for Content Delivery & for security & performance.

## Step #4: Verify and Test the Website
- Open a browser and visit your domain (https://example.com).
- If it doesn't work immediately, wait for DNS propagation (~30 mins to a few hours).

  🎉 DONE! Your Website Is Live



