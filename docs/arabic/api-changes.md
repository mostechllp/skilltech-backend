# API changes for Arabic translations

This document tracks all changes made to the API response schemas to include the new Arabic translation fields.

---

## 1. Category Endpoint (`/api/categories/`)

### Affected Serializer
- `CategorySerializer` and `CategorySerializer2`

### Changes
- Automatically includes `name_ar` (type: `string`, nullable: `true`) inside the category payload.

### Example Response
```json
[
  {
    "id": 1,
    "name": "Wall Mounts",
    "name_ar": "حوامل جدارية",
    "slug": "wall-mounts",
    "image": "/media/categories/wall_mounts.png",
    "show_in_home": true,
    "show_in_explore_home": true,
    "show_in_footer": true,
    "active": true,
    "order": "1.000",
    "homepage_order": "1.000",
    "meta_title": "Premium Wall Mounts",
    "meta_description": "Best wall mounts for TVs.",
    "meta_image": null
  }
]
```

---

## 2. Main Categories Endpoint (`/api/maincategories/`)

### Affected Serializer
- `MainCategorySerializer` -> `CategorySerializer`

### Changes
- The nested category objects now include `name_ar`.

---

## 3. Subcategories Endpoint (`/api/subcategories/`)

### Affected Serializer
- `SubCategorySerializer` -> `CategorySerializer2`

### Changes
- The nested category object now includes `name_ar`.

---

## 4. Product List Endpoint (`/api/products/`)

### Affected Serializer
- `ProductListSerializer`

### Changes
- Added a root-level field `category_ar` mapping to the category's Arabic name (`subcategory.category.name_ar`).

### Example Response
```json
[
  {
    "id": 1,
    "name": "Tilt TV Wall Mount",
    "title": "Tilt TV Wall Mount",
    "slug": "tilt-tv-wall-mount",
    "slug_path": "wall-mounts/tilt/tilt-tv-wall-mount",
    "main_image": "/media/products/tilt_mount.png",
    "main_image_alt": "Tilt TV Mount",
    "short_description": "Tilting bracket.",
    "subcategory_slug": "tilt-mounts",
    "category_slug": "wall-mounts",
    "category": "Wall Mounts",
    "category_ar": "حوامل جدارية",
    "show_in_home": true,
    "active": true,
    "order": "1.000",
    "show_economic": false
  }
]
```
