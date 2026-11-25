# Getting Started with GitHub Copilot

_Get started using GitHub Copilot in less than an hour._

## Windows inspirational quote notifications

The standalone `src/quote-notifier.ps1` utility shows a random, locally stored
inspirational quote as a Windows notification every four hours during the day:
**8 AM, noon, and 4 PM, in your local time zone**, every day. It does not change
the school activities website or require Python, extra packages, or internet access.

On Windows 10 or 11, open PowerShell in this repository and run:

```powershell
# Preview a quote without showing a notification or installing anything.
powershell.exe -NoProfile -ExecutionPolicy RemoteSigned -File .\src\quote-notifier.ps1 -Action Preview

# Install (or update) the scheduled task for the current signed-in user.
powershell.exe -NoProfile -ExecutionPolicy RemoteSigned -File .\src\quote-notifier.ps1 -Action Install

# Show a notification now (only between 8 AM and 8 PM).
powershell.exe -NoProfile -STA -ExecutionPolicy RemoteSigned -File .\src\quote-notifier.ps1

# Remove the scheduled task.
powershell.exe -NoProfile -ExecutionPolicy RemoteSigned -File .\src\quote-notifier.ps1 -Action Uninstall
```

Keep the script at the same location after installing; rerun `Install` if you move
it. The task runs only while you are signed in, without administrator privileges
or a continuously running background process. Missed notifications while asleep,
powered off, or signed out are not replayed. Notifications outside 8 AM–8 PM are
suppressed, including manual task runs.

Allow notifications in Windows settings and turn off Do Not Disturb/Focus Assist
if you do not see them. Windows controls the notification's display duration.
If Windows marks a downloaded script as blocked, review it and use
`Unblock-File .\src\quote-notifier.ps1` before running it. Organization execution
policies may prevent scripts from running.

## Welcome

- **Who is this for**: Developers at any experience level looking to accelerate their code workflow.
- **What you'll learn**: The different ways to interact with Copilot to explain, write, plan, and develop code.
- **What you'll build**: You will guide Copilot to update Mergington High School's extracurricular activities website.
- **Prerequisites**:
  - Skills exercise: [Introduction to GitHub](https://github.com/skills/introduction-to-github)
  - Familiarity with [VS Code](https://code.visualstudio.com/)
  - Basic coding principles
- **How long**: This exercise takes less than one hour to complete.

In this exercise, you will:

1. Use a preconfigured Codespace to run VS Code in your browser.
1. Learn different interaction options to develop and plan with GitHub Copilot.
1. Use Copilot to summarize and review your pull request.

### How to start this exercise

Simply copy the exercise to your account, then give your favorite Octocat (Mona) **about 20 seconds** to prepare the first lesson, then **refresh the page**.

[![](https://img.shields.io/badge/Copy%20Exercise-%E2%86%92-1f883d?style=for-the-badge&logo=github&labelColor=197935)](https://github.com/new?template_owner=skills&template_name=getting-started-with-github-copilot&owner=%40me&name=skills-getting-started-with-github-copilot&description=Exercise:+Get+started+using+GitHub+Copilot&visibility=public)

<details>
<summary>Having trouble? 🤷</summary><br/>

When copying the exercise, we recommend the following settings:

- For owner, choose your personal account or an organization to host the repository.

- We recommend creating a public repository, since private repositories will use Actions minutes.
   
If the exercise isn't ready in 20 seconds, please check the [Actions](../../actions) tab.

- Check to see if a job is running. Sometimes it simply takes a bit longer.

- If the page shows a failed job, please submit an issue. Nice, you found a bug! 🐛

</details>

---

&copy; 2025 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)