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

---

## 5. Subcategories Endpoint (`/api/subcategories/`)

### Affected Serializer
- `SubCategorySerializer`

### Changes
- Automatically includes `name_ar` (type: `string`, nullable: `true`) inside the subcategory payload.

### Example Response
```json
[
  {
    "id": 1,
    "category_slug": "wall-mounts",
    "products_count": 5,
    "category": {
      "id": 1,
      "name": "Wall Mounts",
      "name_ar": "حوامل جدارية",
      "slug": "wall-mounts"
    },
    "name": "Fixed TV Mounts",
    "name_ar": "حوامل التلفزيون الثابتة",
    "slug": "fixed-mounts",
    "image": "/media/subcategories/fixed_mounts.png",
    "active": true,
    "order": "1.000",
    "multi_expand": false,
    "meta_title": "Fixed TV Mounts",
    "meta_description": "Slim profile fixed brackets.",
    "meta_keywords": "fixed mounts"
  }
]
```

---

## 6. Product List Endpoint (`/api/products/`)

### Affected Serializer
- `ProductListSerializer`

### Changes
- Added a root-level field `subcategory_name_ar` mapping to the subcategory's Arabic name (`subcategory.name_ar`).

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
    "subcategory_name_ar": "حوامل التلفزيون المائلة",
    "show_in_home": true,
    "active": true,
    "order": "1.000",
    "show_economic": false
  }
]

---

## 7. Offers Endpoint (`/api/offers/`)

### Affected Serializer
- `OfferSerializer`

### Changes
- Automatically includes:
  - `title_ar` (type: `string`, nullable: `true`)
  - `subtitle_ar` (type: `string`, nullable: `true`)
  - `button_text_ar` (type: `string`, nullable: `true`)
  - `button_link_ar` (type: `string`, nullable: `true`)

### Example Response
```json
[
  {
    "id": 1,
    "title": "Special Deal",
    "title_ar": "صفقة خاصة",
    "subtitle": "Limited Time Only",
    "subtitle_ar": "لفترة محدودة فقط",
    "image": "/media/offers/deal.png",
    "button_text": "Explore",
    "button_text_ar": "استكشف",
    "button_link": "/offers/special",
    "button_link_ar": "/ar/offers/special",
    "active": true,
    "order": 1
  }
]
```

---

## 8. Projects Endpoint (`/api/projects/`)

### Affected Serializer
- `ProjectSerializer`

### Changes
- Automatically includes:
  - `title_ar` (type: `string`, nullable: `true`)
  - `subtitle_ar` (type: `string`, nullable: `true`)
  - `location_ar` (type: `string`, nullable: `true`)

### Example Response
```json
[
  {
    "id": 1,
    "title": "Smart Office Setup",
    "title_ar": "إعداد المكتب الذكي",
    "subtitle": "Interactive workspace integration",
    "subtitle_ar": "تكامل مساحة العمل التفاعلية",
    "location": "Dubai, UAE",
    "location_ar": "دبي، الإمارات العربية المتحدة",
    "image": "/media/projects/office.png",
    "order": 1,
    "active": true
  }
]
```

---

## 9. Service FAQs Endpoint (`/api/service-faqs/`)

### Affected Serializer
- `ServiceFAQSerializer`

### Changes
- Includes:
  - `question_ar` (type: `string`, nullable: `true`)
  - `answer_ar` (type: `string`, nullable: `true`)

### Example Response
```json
[
  {
    "id": 1,
    "question": "What is the warranty period?",
    "question_ar": "ما هي فترة الضمان؟",
    "answer": "We offer a 2-year warranty on all installations.",
    "answer_ar": "نحن نقدم ضمان لمدة عامين على جميع عمليات التركيب.",
    "order": 1
  }
]
```

---

## 10. News Posts Endpoint (`/api/news-posts/`)

### Affected Serializer
- `NewsPostSerializer`

### Changes
- Includes:
  - `title_ar` (type: `string`, nullable: `true`)
  - `content_ar` (type: `string`, nullable: `true`)

### Example Response
```json
[
  {
    "id": 1,
    "category": {
      "id": 1,
      "name": "General News"
    },
    "title": "New Installation Methods Launched",
    "title_ar": "إطلاق طرق تركيب جديدة",
    "slug": "new-installation-methods-launched",
    "cover_image": "/media/news/news1.png",
    "content": "We have introduced state of the art wall mounting techniques.",
    "content_ar": "لقد أدخلنا أحدث تقنيات التركيب على الجدران.",
    "video_url": null,
    "status": "published",
    "published_at": "2026-06-24T12:00:00Z",
    "created_at": "2026-06-24T10:00:00Z",
    "order": 1
  }
]
```

---

## 11. Blog Posts Endpoint (`/api/blogs/`)

### Affected Serializer
- `BlogPostSerializer`

### Changes
- Includes:
  - `title_ar` (type: `string`, nullable: `true`)
  - `image_ar` (type: `string`, nullable: `true`, fallback: `image`)
  - `content_ar` (type: `string`, nullable: `true`)
  - `short_description_ar` (type: `string`, nullable: `true`)
  - `author_ar` (type: `string`, nullable: `true`)

### Example Response
```json
[
  {
    "id": 1,
    "title": "Why You Need a Professional TV Mount",
    "title_ar": "لماذا تحتاج إلى حامل تلفزيون احترافي",
    "slug": "why-you-need-a-professional-tv-mount",
    "image": "/media/blog/mount1.png",
    "image_ar": "/media/blog/mount1.png",
    "content": "Choosing the right wall type and mounting is critical for safety...",
    "content_ar": "يعد اختيار نوع الجدار والتركيب المناسبين أمرًا بالغ الأهمية للسلامة...",
    "short_description": "A guide to selecting the best TV mount.",
    "short_description_ar": "دليل لاختيار أفضل حامل تلفزيون.",
    "tags": ["Tech", "News"],
    "author": "Admin",
    "author_ar": "المدير",
    "created_at": "2026-06-24T10:00:00Z",
    "active": true
  }
]
```

---

## 12. Global Locations Endpoint (`/api/global-locations/`)

### Affected Serializer
- `GlobalLocationSerializer`

### Changes
- Includes:
  - `country_ar` (type: `string`, nullable: `true`)
  - `address_ar` (type: `string`, nullable: `true`)

### Example Response
```json
[
  {
    "id": 1,
    "country": "United Arab Emirates",
    "country_ar": "الإمارات العربية المتحدة",
    "address": "Office 402, Business Bay, Dubai, UAE",
    "address_ar": "مكتب 402، الخليج التجاري، دبي، الإمارات العربية المتحدة",
    "email": "info@skilltech.ae",
    "map_iframe": "<iframe>...</iframe>",
    "map_link": "https://maps.google.com/...",
    "active": true,
    "order": 1
  }
]
```

---

## 13. Site Settings Endpoint (`/api/settings/`)

### Affected Serializer
- `SiteSettingsSerializer`

### Changes
- Includes:
  - `address_heading_ar` (type: `string`, nullable: `true`)
  - `address_ar` (type: `string`, nullable: `true`)

### Example Response
```json
[
  {
    "id": 1,
    "email": "info@skilltech.ae",
    "phone": "+97141234567",
    "address_heading": "Our Office",
    "address_heading_ar": "مكتبنا",
    "address": "Office 402, Business Bay, Dubai, UAE",
    "address_ar": "مكتب 402، الخليج التجاري، دبي، الإمارات العربية المتحدة",
    "google_map_link": "https://maps.google.com/..."
  }
]
```

---

## 14. Arms Endpoint (`/api/arms/`)

### Affected Serializer
- `ArmSerializer`

### Changes
- Includes:
  - `name_ar` (type: `string`, nullable: `true`)

### Example Response
```json
[
  {
    "id": 1,
    "name": "Single Arm",
    "name_ar": "ذراع واحد",
    "order": "1.000",
    "active": true,
    "show_in_articulating": true,
    "show_in_ergonomic": true,
    "slug": "single-arm"
  }
]
```

---

## 15. Catalogues Endpoint (`/api/catalogues/`)

### Affected Serializer
- `CatalogueSerializer`

### Changes
- Includes:
  - `title_ar` (type: `string`, nullable: `true`)

### Example Response
```json
[
  {
    "id": 1,
    "title": "Main Product Catalogue",
    "title_ar": "كتالوج المنتجات الرئيسي",
    "thumbnail": "/media/catalogues/thumbnails/cover.png",
    "file": "/media/catalogues/files/catalogue.pdf",
    "order": 1,
    "active": true
  }
]
```

---

## 16. Certificates Endpoint (`/api/certificates/`)

### Affected Serializer
- `CertificateSerializer`

### Changes
- Includes:
  - `title_ar` (type: `string`, nullable: `true`)

### Example Response
```json
[
  {
    "id": 1,
    "title": "ISO 9001 Certification",
    "title_ar": "شهادة الأيزو 9001",
    "thumbnail": "/media/certificates/thumbnails/iso.png",
    "file": "/media/certificates/files/iso.pdf",
    "order": 1,
    "active": true
  }
]
```

---

## 17. Features Endpoint (`/api/features/` or embedded in product lists)

### Affected Serializer
- `FeatureSerializer`

### Changes
- Includes:
  - `title_ar` (type: `string`, nullable: `true`)

### Example Response
```json
[
  {
    "id": 1,
    "title": "Max Load Capacity",
    "title_ar": "أقصى سعة تحميل",
    "order": "1.000"
  }
]
```

---

## 18. Gallery Endpoint (`/api/gallery/` or embedded in category lists)

### Affected Serializer
- `GallerySerializer`

### Changes
- Includes:
  - `title_ar` (type: `string`, nullable: `true`)

### Example Response
```json
[
  {
    "id": 1,
    "category": 2,
    "category_slug": "tv-mounts",
    "image": "/media/gallery/photo.png",
    "title": "Living Room Installation",
    "title_ar": "تركيب غرفة المعيشة",
    "created_at": "2026-06-25T12:00:00Z"
  }
]
```

---

## 19. Statistics Endpoint (`/api/statistics/`)

### Affected Serializer
- `StatisticSerializer`

### Changes
- Includes:
  - `value_ar` (type: `string`, nullable: `true`)
  - `label_ar` (type: `string`, nullable: `true`)

### Example Response
```json
[
  {
    "id": 1,
    "value": 100,
    "value_ar": "١٠٠",
    "label": "Projects Completed",
    "label_ar": "المشاريع المنجزة",
    "suffix": "+",
    "icon": "/media/statistics/projects.png",
    "order": 1,
    "active": true
  }
]
```

---

## 20. Main Categories Endpoint (`/api/main-categories/` or nested in product paths)

### Affected Serializer
- `MainCategorySerializer`

### Changes
- Includes:
  - `name_ar` (type: `string`, nullable: `true`)

### Example Response
```json
[
  {
    "id": 1,
    "name": "TV Mounts",
    "name_ar": "حوامل التلفزيون",
    "slug": "tv-mounts",
    "order": "1.000",
    "categories": []
  }
]
```

---

## 21. Service Statistics Endpoint (`/api/service-statistics/`)

### Affected Serializer
- `ServiceStatisticSerializer`

### Changes
- Includes:
  - `value_ar` (type: `string`, nullable: `true`)
  - `label_ar` (type: `string`, nullable: `true`)

### Example Response
```json
[
  {
    "id": 1,
    "value": 500,
    "value_ar": "٥٠٠",
    "label": "Services Completed",
    "label_ar": "الخدمات المكتملة",
    "suffix": "+",
    "icon": "/media/service_statistics/services.png",
    "order": 1,
    "active": true
  }
]
```

---

## 22. Services Endpoint (`/api/services/`)

### Affected Serializer
- `ServiceSerializer`
- `InstallationTypeSerializer`
- `TVSizeSerializer`
- `AvailableTimeSerializer`

### Changes
- Includes:
  - `name_ar` (type: `string`, nullable: `true`)
  - `description_ar` (type: `string`, nullable: `true`)
  - Nested fields in `installation_types`: `name_ar` (type: `string`, nullable: `true`)
  - Nested fields in `tv_sizes`: `size_ar` (type: `string`, nullable: `true`)
  - Nested fields in `available_times`: `time_slot_ar` (type: `string`, nullable: `true`)

### Example Response
```json
[
  {
    "id": 1,
    "name": "TV Mounting Service",
    "name_ar": "خدمة تركيب التلفزيون",
    "description": "Professional TV wall mounting.",
    "description_ar": "تركيب التلفزيون على الحائط بشكل احترافي.",
    "active": true,
    "installation_types": [
      {
        "id": 1,
        "name": "Drywall Installation",
        "name_ar": "التركيب على الجدران الجافة"
      }
    ],
    "tv_sizes": [
      {
        "id": 1,
        "size": "55-65 inches",
        "size_ar": "٥٥-٦٥ بوصة"
      }
    ],
    "available_times": [
      {
        "id": 1,
        "time_slot": "9:00 AM - 12:00 PM",
        "time_slot_ar": "٩:٠٠ صباحًا - ١٢:٠٠ مساءً"
      }
    ]
  }
]
```

---

## 23. Homepage Banners Endpoint (`/api/homepage-banners/`)

### Affected Serializer
- `HomepageBannerSerializer`

### Changes
- Includes:
  - `image_ar` (type: `string`, nullable: `true`)
  - Auto-fallback logic: if `image_ar` is not uploaded, the serializer returns the original English `image` in `image_ar`.

### Example Response
```json
[
  {
    "id": 1,
    "link": "/products",
    "image": "/media/banners/banner.png",
    "image_ar": "/media/banners/banner.png",
    "image_alt": "Mounting Solutions banner",
    "active": true,
    "order": "1.000"
  }
]
```

---

## 24. Products Endpoints (`/api/products/`, `/api/products/<slug>/`)

### Affected Serializer
- `ProductListSerializer`
- `ProductDetailSerializer`
- `SimilarProductSerializer`

### Changes
- Includes:
  - `title_ar` (type: `string`, nullable: `true`)
  - `short_description_ar` (type: `string`, nullable: `true`)
  - `description_ar` (type: `string`, nullable: `true`) (detail endpoint only)
  - `tags_ar` (type: `string`, nullable: `true`) (detail endpoint only)

### Example Response
```json
{
  "id": 1,
  "name": "SH 380R",
  "title": "360 Rotate Wall Mount",
  "title_ar": "حامل حائط يدور ٣٦٠ درجة",
  "slug": "sh-380r",
  "short_description": "Flexible rotation wall mount",
  "short_description_ar": "حامل حائط مرن الدوران",
  "description": "Premium 360 rotation flat screen tv mount",
  "description_ar": "حامل تلفزيون شاشة مسطحة بدوران ٣٦٠ درجة ممتاز",
  "tags": "Mount, 360",
  "tags_ar": "حامل, ٣٦٠"
}
```

---

## 25. Product Bullet Features Endpoint (nested under product detail `/api/products/<slug>/`)

### Affected Serializer
- `ProductBulletFeatureSerializer`

### Changes
- Includes:
  - `title_ar` (type: `string`, nullable: `true`)
  - `text_ar` (type: `string`, nullable: `true`)

### Example Response snippet
```json
{
  "bullet_features": [
    {
      "id": 1,
      "title": "VESA Compatible",
      "title_ar": "متوافق مع فيسا",
      "text": "Supports up to 400x400mm",
      "text_ar": "يدعم حتى ٤٠٠×٤٠٠ مم",
      "order": "1.000"
    }
  ]
}
```

---

## 26. Product Specifications Endpoint (nested under product detail `/api/products/<slug>/`)

### Affected Serializer
- `ProductSpecificationSerializer`

### Changes
- Includes:
  - `key_ar` (type: `string`, nullable: `true`)
  - `value_ar` (type: `string`, nullable: `true`)

### Example Response snippet
```json
{
  "specifications": [
    {
      "key": "Material",
      "key_ar": "المادة",
      "value": "Solid Steel",
      "value_ar": "فولاذ صلب"
    }
  ]
}
```
```
```
```
```

