this file is created for tracking model changes.
all the model changes will be recorded here.

the main purpose is to check the database changes and model changes in the Arabic language.
also need to find out the apis used and update the database changes there.

## Documented Changes

### 1. Category Model
- **Model Name**: `Category`
- **File**: `catalog/models.py`
- **Fields Added**:
  - `name_ar` (`CharField`, `max_length=100`, `null=True`, `blank=True`): Stores the Arabic translation of the category name.
- **Migration Details**:
  - Migration file: `catalog/migrations/0002_category_name_ar.py`
  - Applied: Yes

### 2. SubCategory Model
- **Model Name**: `SubCategory`
- **File**: `catalog/models.py`
- **Fields Added**:
  - `name_ar` (`CharField`, `max_length=100`, `null=True`, `blank=True`): Stores the Arabic translation of the subcategory name.
- **Migration Details**:
  - Migration file: `catalog/migrations/0003_subcategory_name_ar.py`
  - Applied: Yes

### 3. Offer Model
- **Model Name**: `Offer`
- **File**: `catalog/models.py`
- **Fields Added**:
  - `title_ar` (`CharField`, `max_length=100`, `null=True`, `blank=True`): Stores the Arabic translation of the offer title.
  - `subtitle_ar` (`CharField`, `max_length=100`, `null=True`, `blank=True`): Stores the Arabic translation of the offer subtitle.
  - `button_text_ar` (`CharField`, `max_length=50`, `null=True`, `blank=True`): Stores the Arabic translation of the button text.
  - `button_link_ar` (`CharField`, `max_length=200`, `null=True`, `blank=True`): Stores the Arabic translation of the button redirect link.
- **Migration Details**:
  - Migration file: `catalog/migrations/0004_offer_button_link_ar_offer_button_text_ar_and_more.py`
  - Applied: Yes

### 4. Project Model
- **Model Name**: `Project`
- **File**: `catalog/models.py`
- **Fields Added**:
  - `title_ar` (`CharField`, `max_length=100`, `null=True`, `blank=True`): Stores the Arabic translation of the project title.
  - `subtitle_ar` (`CharField`, `max_length=100`, `null=True`, `blank=True`): Stores the Arabic translation of the project subtitle.
  - `location_ar` (`CharField`, `max_length=100`, `null=True`, `blank=True`): Stores the Arabic translation of the project location.
- **Migration Details**:
  - Migration file: `catalog/migrations/0005_project_location_ar_project_subtitle_ar_and_more.py`
  - Applied: Yes

### 5. ServiceFAQ Model
- **Model Name**: `ServiceFAQ`
- **File**: `catalog/models.py`
- **Fields Added**:
  - `question_ar` (`CharField`, `max_length=255`, `null=True`, `blank=True`): Stores the Arabic translation of the FAQ question.
  - `answer_ar` (`TextField`, `null=True`, `blank=True`): Stores the Arabic translation of the FAQ answer.
- **Migration Details**:
  - Migration file: `catalog/migrations/0006_servicefaq_answer_ar_servicefaq_question_ar.py`
  - Applied: Yes

### 6. NewsPost Model
- **Model Name**: `NewsPost`
- **File**: `catalog/models.py`
- **Fields Added**:
  - `title_ar` (`CharField`, `max_length=255`, `null=True`, `blank=True`): Stores the Arabic translation of the news post title.
  - `content_ar` (`TextField`, `null=True`, `blank=True`): Stores the Arabic translation of the news post main content.
- **Migration Details**:
  - Migration file: `catalog/migrations/0007_newspost_content_ar_newspost_title_ar.py`
  - Applied: Yes

### 7. BlogPost Model
- **Model Name**: `BlogPost`
- **File**: `catalog/models.py`
- **Fields Added**:
  - `title_ar` (`CharField`, `max_length=200`, `null=True`, `blank=True`): Stores the Arabic translation of the blog post title.
  - `image_ar` (`ImageField`, `null=True`, `blank=True`): Stores the Arabic translation/localized image of the blog post. If empty, fallback to original image.
  - `content_ar` (`TextField`, `null=True`, `blank=True`): Stores the Arabic translation of the blog post main content.
  - `short_description_ar` (`TextField`, `null=True`, `blank=True`): Stores the Arabic translation of the short description.
  - `author_ar` (`CharField`, `max_length=100`, `null=True`, `blank=True`): Stores the Arabic translation of the author name.
- **Migration Details**:
  - Migration file: `catalog/migrations/0008_blogpost_author_ar_blogpost_content_ar_and_more.py`
  - Applied: Yes

### 8. GlobalLocation Model
- **Model Name**: `GlobalLocation`
- **File**: `catalog/models.py`
- **Fields Added**:
  - `country_ar` (`CharField`, `max_length=100`, `null=True`, `blank=True`): Stores the Arabic translation of the country name.
  - `address_ar` (`TextField`, `null=True`, `blank=True`): Stores the Arabic translation of the location address.
- **Migration Details**:
  - Migration file: `catalog/migrations/0009_globallocation_address_ar_globallocation_country_ar.py`
  - Applied: Yes

### 9. SiteSettings Model
- **Model Name**: `SiteSettings`
- **File**: `catalog/models.py`
- **Fields Added**:
  - `address_heading_ar` (`CharField`, `max_length=100`, `null=True`, `blank=True`): Stores the Arabic translation of the address section heading.
  - `address_ar` (`TextField`, `null=True`, `blank=True`): Stores the Arabic translation of the address.
- **Migration Details**:
  - Migration file: `catalog/migrations/0010_sitesettings_address_ar_and_more.py`
  - Applied: Yes

### 10. Arm Model
- **Model Name**: `Arm`
- **File**: `catalog/models.py`
- **Fields Added**:
  - `name_ar` (`CharField`, `max_length=50`, `null=True`, `blank=True`): Stores the Arabic translation of the arm name.
- **Migration Details**:
  - Migration file: `catalog/migrations/0011_arm_name_ar.py`
  - Applied: Yes

### 11. Catalogue Model
- **Model Name**: `Catalogue`
- **File**: `catalog/models.py`
- **Fields Added**:
  - `title_ar` (`CharField`, `max_length=100`, `null=True`, `blank=True`): Stores the Arabic translation of the catalogue title.
- **Migration Details**:
  - Migration file: `catalog/migrations/0012_catalogue_title_ar.py`
  - Applied: Yes

### 12. Certificate Model
- **Model Name**: `Certificate`
- **File**: `catalog/models.py`
- **Fields Added**:
  - `title_ar` (`CharField`, `max_length=100`, `null=True`, `blank=True`): Stores the Arabic translation of the certificate title.
- **Migration Details**:
  - Migration file: `catalog/migrations/0013_certificate_title_ar.py`
  - Applied: Yes

### 13. Feature Model
- **Model Name**: `Feature`
- **File**: `catalog/models.py`
- **Fields Added**:
  - `title_ar` (`CharField`, `max_length=100`, `null=True`, `blank=True`): Stores the Arabic translation of the feature title.
- **Migration Details**:
  - Migration file: `catalog/migrations/0014_feature_title_ar.py`
  - Applied: Yes

### 14. Gallery Model
- **Model Name**: `Gallery`
- **File**: `catalog/models.py`
- **Fields Added**:
  - `title_ar` (`CharField`, `max_length=100`, `null=True`, `blank=True`): Stores the Arabic translation of the gallery image title.
- **Migration Details**:
  - Migration file: `catalog/migrations/0015_gallery_title_ar.py`
  - Applied: Yes

### 15. HomeStatistic Model
- **Model Name**: `HomeStatistic`
- **File**: `catalog/models.py`
- **Fields Added**:
  - `value_ar` (`CharField`, `max_length=50`, `null=True`, `blank=True`): Arabic translation or override for the value.
  - `label_ar` (`CharField`, `max_length=100`, `null=True`, `blank=True`): Arabic translation of the statistic label.
- **Migration Details**:
  - Migration file: `catalog/migrations/0016_homestatistic_label_ar_homestatistic_value_ar.py`
  - Applied: Yes

### 16. MainCategory Model
- **Model Name**: `MainCategory`
- **File**: `catalog/models.py`
- **Fields Added**:
  - `name_ar` (`CharField`, `max_length=100`, `null=True`, `blank=True`): Arabic translation of the main category name.
- **Migration Details**:
  - Migration file: `catalog/migrations/0017_maincategory_name_ar.py`
  - Applied: Yes

### 17. ServiceStatistic Model
- **Model Name**: `ServiceStatistic`
- **File**: `catalog/models.py`
- **Fields Added**:
  - `value_ar` (`CharField`, `max_length=50`, `null=True`, `blank=True`): Arabic translation or override for the value.
  - `label_ar` (`CharField`, `max_length=100`, `null=True`, `blank=True`): Arabic translation of the statistic label.
- **Migration Details**:
  - Migration file: `catalog/migrations/0018_servicestatistic_label_ar_and_more.py`
  - Applied: Yes



