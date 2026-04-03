from django import forms
from .models import Product, Category, SubCategory

class ProductAdminForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Select Category"
    )

    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.subcategory:
            self.fields['category'].initial = self.instance.subcategory.category
            # Optionally filter subcategory queryset to current category
            # self.fields['subcategory'].queryset = SubCategory.objects.filter(
            #     category=self.instance.subcategory.category
            # )
        elif 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass

    # class Media:
    #     js = ('js/category_filter.js',)
