# Module 1 resource page

A static, responsive resource library generated with Python. No Python packages, JavaScript libraries, API keys or build service required. Python runs on your computer; GitHub Pages serves the generated HTML and PDF.

## Preview

Open `index.html` in a browser. The page works directly from disk, including the bundled PDF. Click a topic tile or section heading to reveal its explanation and resources. All resource links open in a new tab.

## Edit and rebuild

1. Edit `resources.json` to change topic explanations, questions and resource links.
2. Place additional PDFs in `assets/` and use relative URLs such as `assets/example.pdf`. Append `#page=43` to suggest a starting page (support depends on the PDF viewer).
3. From this folder run:

```sh
python3 build.py
```

Edit `template.html` for colours, layout, the introductory text around the topics, and the activity. The title and subtitle come from the JSON file. The three summary badges in the template are manually maintained.

## Publish on GitHub Pages

1. Create or choose a GitHub repository.
2. Upload this folder's **contents** to the root of the repository, preserving the `assets/` directory. Include `index.html`, `assets/EnergyandAI.pdf` and `.nojekyll`; keep the Python script, template and JSON there too for future edits.
3. In the repository's Settings → Pages, choose deployment from a branch, select `main` and `/ (root)`, then save. GitHub account/repository settings may affect which publishing options are available.
4. Use the Pages address GitHub displays once deployment finishes.

After future edits, run the Python script again and upload/commit the changed files, including the rebuilt `index.html`. There is no server-side Python to configure and no GitHub Actions workflow is required.

## Contents and editorial notes

- The two video URLs and Module 1 topics come from the supplied resources document and user message. Videos use descriptive topic labels, not independently verified official video titles. Playback availability was not verified.
- The attached IEA report is bundled unchanged. Attribution: IEA (2025), Energy and AI, IEA, Paris. CC BY 4.0. Source: https://www.iea.org/reports/energy-and-ai ; licence: https://creativecommons.org/licenses/by/4.0/
- Reading suggestions, short introductions and discussion prompts were drafted for this prototype. They can be revised in `resources.json`.
- The worldwide LLM adoption activity comes from the course outline; its starting questions are suggestions.
- The source course-planning documents are not included in the public site.
- No site has been published and no GitHub repository has been modified.

Publishing reference: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

Validation: Python generation and HTML structure/local resource checks passed. Automated visual/browser interaction checks could not run because the available browser failed to launch.
