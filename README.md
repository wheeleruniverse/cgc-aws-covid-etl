# AWS COVID-19 ETL Pipeline

A serverless, event-driven ETL pipeline for processing COVID-19 data from the New York Times and Johns Hopkins datasets using AWS services.

## 🏆 Cloud Guru Challenge Submission

This project was built for the September 2020 [#CloudGuruChallenge](https://www.pluralsight.com/resources/blog/cloud/cloudguruchallenge-python-aws-etl) on Event-Driven Python on AWS.

**Blog Post**: [My September Cloud Guru Challenge Experience](https://dev.to/wheeleruniverse/my-september-cloud-guru-challenge-experience-l2j)

## 📋 Overview

This ETL pipeline automatically processes daily COVID-19 data for the United States, combining case and death statistics from the New York Times dataset with recovery data from Johns Hopkins University. The pipeline runs daily, performs data transformations, and stores the results in DynamoDB with visualization capabilities through AWS QuickSight.

### Key Features
- **Automated Daily Processing**: Scheduled Lambda function triggered by CloudWatch Events
- **Multiple Data Sources**: Integrates NYT and Johns Hopkins COVID-19 datasets
- **Data Transformation**: Cleans, joins, and filters data using Python
- **Serverless Architecture**: Built entirely on AWS managed services
- **Error Handling**: Graceful failure handling with SNS notifications
- **Data Visualization**: QuickSight dashboard for data analysis

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│   CloudWatch    │────▶│    Lambda    │────▶│  DynamoDB   │
│   Event Rule    │     │   Function   │     │    Table    │
└─────────────────┘     └──────┬───────┘     └─────────────┘
                               │                      │
                               ▼                      ▼
                        ┌──────────────┐       ┌───────────┐
                        │     SNS      │       │    S3     │
                        │    Topic     │       │  Bucket   │
                        └──────────────┘       └─────┬─────┘
                                                     │
                                                     ▼
                                              ┌─────────────┐
                                              │ QuickSight  │
                                              │  Dashboard  │
                                              └─────────────┘
```

## 🛠️ Technologies Used

- **AWS Lambda**: Serverless compute for ETL processing
- **Amazon DynamoDB**: NoSQL database for storing processed data
- **Amazon S3**: Object storage for JSON data files
- **AWS CloudWatch Events**: Scheduled triggers for daily processing
- **Amazon SNS**: Notifications for job completion and errors
- **AWS QuickSight**: Business intelligence for data visualization
- **Python 3.x**: Core programming language
- **Boto3**: AWS SDK for Python

## 🚀 Getting Started

### Prerequisites

- AWS Account with appropriate permissions
- Python 3.8 or higher
- AWS CLI configured with credentials
- Boto3 library installed

## 📊 Data Sources

### New York Times COVID-19 Data
- **URL**: https://github.com/nytimes/covid-19-data/blob/master/us.csv
- **Contains**: Daily US case counts and deaths
- **Update Frequency**: Daily

### Johns Hopkins COVID-19 Data
- **URL**: https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv
- **Contains**: Global COVID-19 data including recoveries
- **Used For**: Recovery data only (US subset)

## 🔄 ETL Process

### 1. Extract
- Downloads latest CSV files from NYT and Johns Hopkins repositories
- Loads data into memory for processing

### 2. Transform
- **Date Conversion**: Converts date strings to proper date objects
- **Data Joining**: Merges NYT case/death data with Johns Hopkins recovery data
- **Filtering**: Removes non-US data and aligns date ranges
- **Data Cleaning**: Handles missing values and data inconsistencies

### 3. Load
- **Initial Load**: Loads complete historical dataset on first run
- **Incremental Updates**: Adds only new daily data on subsequent runs
- **Dual Storage**: Writes to both DynamoDB and S3 (as JSON)

## 🔔 Monitoring & Notifications

The pipeline uses Amazon SNS for notifications:
- **Success Notifications**: Include number of rows processed
- **Error Notifications**: Detail failure reasons and stack traces
- **Retry Logic**: Failed processing attempts are retried on next run

## 📈 Data Visualization

While QuickSight dashboards cannot be made public without additional authentication infrastructure, the pipeline creates visualizations for:
- Daily new cases trend
- Cumulative cases over time
- Death rate analysis
- Recovery rate tracking
- State-by-state comparisons (if extended)

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

Tests include:
- Unit tests for transformation logic
- Integration tests for AWS services
- Error handling scenarios
- Edge case validation

## 💡 Lessons Learned

### Challenges Encountered

1. **DynamoDB Limitations**: 
   - No native support for incremental loads without full table scans
   - QuickSight requires Enterprise edition for VPC resources

2. **QuickSight Restrictions**:
   - No direct DynamoDB integration
   - Public dashboards require embedded analytics

3. **Data Consistency**:
   - NYT and Johns Hopkins data have slight discrepancies
   - Date alignment issues between datasets

### Alternative Approaches Considered

- **Aurora Serverless**: Would provide SQL capabilities but adds VPC complexity
- **AWS Glue**: More robust ETL but overkill for this use case
- **Athena + S3**: Could provide serverless SQL queries on data lake

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [A Cloud Guru](https://acloudguru.com/) for the challenge framework
- [New York Times](https://github.com/nytimes/covid-19-data) for maintaining COVID-19 data
- [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19) for global COVID-19 tracking
- AWS community for guidance and support

## 📬 Contact

- **GitHub**: [@wheeleruniverse](https://github.com/wheeleruniverse)
- **Blog**: [dev.to/wheeleruniverse](https://dev.to/wheeleruniverse)

---

*Built with ❤️ as part of the #CloudGuruChallenge*
