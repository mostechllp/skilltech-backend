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

