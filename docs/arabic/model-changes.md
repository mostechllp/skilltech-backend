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



