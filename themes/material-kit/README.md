

## Page metadata

> Fontawesome

Sets the fontawesome icon shown in the menu. No icon is shown when this value is not set.

## Settings

> SOCIAL

A list of tuples (Social network name, URL, title) to appear in the “social” section. 
The social network name is used to set the fontawesome icon and the title is shown when the user hovers over the icon.

See the [FontAwesome gallery](https://fontawesome.com/icons?d=gallery&m=free) for all the icons you can use.

```python
SOCIAL = (('linkedin', 'https://www.linkedin.com/in/me', 'Join my network'),
          ('github', 'https://github.com/me', 'Follow me on GitHub'),)
```

> ARTICLES_ON_HOMEPAGE

Sets the maximum number of articles that will be shown on the homepage

> HOMEPAGE_BANNER

Image for the homepage banner. 
Be aware that the directory of this file must be in `STATIC_PATHS`.
A grey area is displayed when the image is not found.


> FAVICON

Path to the favicon icon. This should be a 32x32 png image. 
Be aware that the directory of this file must be in `STATIC_PATHS`.
A default favicon is displayed when the image is not found.