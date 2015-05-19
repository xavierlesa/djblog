.. -*- restructuredtext -*-
.. header::
    nebula
    author: Xavier Lesa <xavier@link-b.com> y Juan Manuel Silva Garretón <juan@link-b.com>

:Authors: Xavier Lesa (xavier@link-b.com) y Juan Manuel Silva Garretón <juan@link-b.com>
:Version: 1.0.0b 

======
Nebula
======
Nebula es un grupo de aplicaciones desarrolladas para funcionar en conjunto
pero también de forma independiente. Ideada para usarse como Blog, CMS, Portal
o Red Social y/u otro fin que se le quiera dar, no hace cafe :(

*La idea detrás de Nebula es poder programar apps que sean fácilmente 
conectables y al mismo tiempo que mantengan una simplicidad. Se busca usar 
modelos abstractos bases para los usos mas comunes de fieds y templates con 
las mismas caracteristicas para que sean reusables*


Common
======

**Common** es una bateria de modelos (abstractos), managers y utils que contiénen 
la base elemental para hacer cualquier APP.

Models
------

MultiSiteBaseModel
------------------

**Fields**

- lang
- site

**Managers**

- objects_for_admin: *retorna un queryset sin filtrar*
- objects: *retorna un queryset filtrando por el site actual o sin site.*
- objects.get_for_site_or_none(): *retorna un queryset filtrando por el site actual.*

**Notas**: éste modelo está suscrito al signal *m2m_change* para evaluar valores únicos, hay una función **check_unique_together_with** que evalúa el *lang*, *site* y el field determinado por **multisite_unique_together** y raisea si ya existe una instancia con los mismo valores. Básicamente funciona igual que un *unique_together* pero con un *m2m*.


BaseModel(MultiSiteBaseModel)
-----------------------------

**Fields**

- pub_date
- up_date
- slug
- is_active
- is_live
- meta_keywords
- meta_description

**Managers**

- objects.live(): *devuelve filtrando por el flag is_live=True*
- objects.active(): *devuelve filtrando por los flags is_live=True y is_active=True*
- objects.latest_update(): *devuelve un queryset ordenando por último modificado*


