---
Title: VS Code Settings
Tags: VS Code, Visual Studio Code
---

VS Code is very configurable. In this post I'll share the configuration I like to use. 

# Auto save

Most of the time I like my IDE to save files automatically instead of having to save each and every file independently. I know, I can save all files, but that's still more work that letting the IDE do it. 

To configure this, just add the following to the main object in `settings.json`:

```json
"files.autoSave": "afterDelay"
```

# Associate language with file extensions

As you can read in the [VS Code documentation](https://code.visualstudio.com/docs/languages/overview#_adding-a-file-extension-to-a-language), you can set a language for each file extension. 

In my example, I would like to add the `.wyam` file extension to `C#`.

```json
"files.associations": {
    "*.wyam": "csharp"
},
```