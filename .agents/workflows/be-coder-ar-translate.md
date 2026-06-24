---
description: be coder for ar translate
---

# Workflow: Arabic Field Translation Implementation

This document outlines the step-by-step workflow for implementing Arabic translation support for specific models and their corresponding APIs in the SkillTech backend repository.

---

## Phase 1: Model Identification & Modification

1. **Identify Target Models**:
   - Obtain the list of target models specified by the developer/user.
   
2. **Add Arabic Fields**:
   - For each target model in `catalog/models.py`, identify the primary string fields (typically `name` or `title`).
   - Add the corresponding Arabic translation fields (e.g., `name_ar` or `title_ar`) with appropriate options (`null=True, blank=True`).
   
3. **Document Model Changes**:
   - Record all additions/modifications in `docs/arabic/model-changes.md`.
   - The documentation for each modified model should include:
     - **Model Name**
     - **Added Field(s)** (e.g., type, character limit, and purpose)
     - **Migration details**

---

## Phase 2: Database Migration

1. **Generate Migrations**:
   - Run the migration generator using Python 3.10:
     ```bash
     venv/bin/python manage.py makemigrations
     ```
2. **Apply Migrations**:
   - Apply the newly generated migrations to the database:
     ```bash
     venv/bin/python manage.py migrate
     ```
3. **Verify Database Schema**:
   - Ensure the new columns are successfully added to the database tables.

---

## Phase 3: API & Serializer Updates

1. **Locate Serializers**:
   - Identify the serializers associated with the modified models (typically located in `catalog/serializers.py` or views).
   
2. **Expose Translation Fields**:
   - Update the serializer's `fields` definition to explicitly include the new Arabic fields (e.g., `name_ar`, `title_ar`).
   - If fields are defined as `__all__`, verify that the fields are automatically exposed and serialize correctly.

3. **Document API Changes**:
   - Record the API additions in `docs/arabic/api-changes.md`.
   - The documentation should cover:
     - **Modified Serializer**
     - **Affected API Endpoint URL**
     - **Example JSON Response** displaying the new Arabic keys.

---

## Phase 4: Admin Panel Integration

1. **Verify Django Admin**:
   - Check `catalog/admin.py` to ensure the new fields are exposed in the administrative panel form for the respective models.
   - Group translation fields together (e.g., grouping `name` and `name_ar` in fields/fieldsets) to keep the admin interface intuitive.

---

## Phase 5: Verification & Validation

```
1. **Verify API Endpoints**:
   - Perform a GET request to the affected endpoints to verify the fields are returned with correct spelling and structure.
