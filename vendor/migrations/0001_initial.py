# Generated by Django 4.2.7 on 2024-02-01 11:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category/')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='vendor.category')),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155)),
                ('image', models.ImageField(upload_to='market/')),
                ('city_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.city')),
            ],
            options={
                'db_table': 'market',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=155)),
                ('description', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('last_price', models.IntegerField()),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
            options={
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(max_length=155)),
                ('image', models.ImageField(upload_to='Shop/')),
                ('city_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.city')),
                ('market_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.market')),
            ],
            options={
                'db_table': 'shop',
            },
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155)),
                ('category_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vendor.category')),
            ],
            options={
                'db_table': 'variation',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True)),
                ('phone_no', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'vendor_user',
            },
        ),
        migrations.CreateModel(
            name='Variation_option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=155)),
                ('varition_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.variation')),
            ],
            options={
                'db_table': 'variation_option',
            },
        ),
        migrations.CreateModel(
            name='Shop_outlet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('landmark', models.CharField(max_length=155)),
                ('latitude', models.CharField(max_length=155)),
                ('longitude', models.CharField(max_length=155)),
                ('postal_code', models.CharField(max_length=155)),
                ('is_default', models.BooleanField()),
                ('address_type', models.CharField(max_length=155)),
                ('address_line1', models.CharField(max_length=155)),
                ('shop_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.shop')),
            ],
            options={
                'db_table': 'shop_outlet',
            },
        ),
        migrations.AddField(
            model_name='shop',
            name='vendor_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.vendor'),
        ),
        migrations.CreateModel(
            name='Product_image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.ImageField(default='default.jpg', upload_to='Product_image/')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.product')),
            ],
            options={
                'db_table': 'product_image',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='VOID',
            field=models.ManyToManyField(to='vendor.variation_option'),
        ),
        migrations.AddField(
            model_name='product',
            name='category_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vendor.category'),
        ),
        migrations.AddField(
            model_name='product',
            name='shop_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.shop'),
        ),
        migrations.AddField(
            model_name='product',
            name='shop_outlet_id',
            field=models.ManyToManyField(related_name='products', to='vendor.shop_outlet'),
        ),
    ]