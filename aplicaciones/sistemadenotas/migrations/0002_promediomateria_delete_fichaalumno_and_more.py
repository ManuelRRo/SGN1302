# Generated by Django 4.1.7 on 2023-06-14 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistemadenotas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promediomateria',
            fields=[
                ('id_alumno', models.OneToOneField(db_column='ID_ALUMNO', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='sistemadenotas.alumno')),
                ('promedio', models.FloatField(blank=True, db_column='PROMEDIO', null=True)),
                ('observacion', models.CharField(blank=True, db_column='OBSERVACION', max_length=50, null=True)),
                ('fecha_edicion', models.DateField(blank=True, db_column='FECHA_EDICION', null=True)),
            ],
            options={
                'db_table': 'promediomateria',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Fichaalumno',
        ),
        migrations.DeleteModel(
            name='Fichadocente',
        ),
    ]
