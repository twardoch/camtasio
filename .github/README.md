# GitHub Actions Workflows

This directory contains GitHub Actions workflow files for the Camtasio project.

## Workflows

### docs.yml - Documentation Building and Deployment

This workflow automatically builds and deploys the MkDocs documentation site:

**Triggers:**
- Push to `master` or `main` branch (changes to `src_docs/**` or workflow file)
- Pull requests to `master` or `main` branch (changes to `src_docs/**`)
- Manual workflow dispatch

**Process:**
1. **Build Job:**
   - Checks out the repository with full git history
   - Sets up Python 3.11 and installs uv package manager
   - Installs MkDocs with Material theme and required plugins
   - Configures Git for the git-revision-date-localized plugin
   - Builds the documentation site from `src_docs/` to `docs/`
   - Uploads the built site as a Pages artifact

2. **Deploy Job:** (only on main/master branch)
   - Deploys the built documentation to GitHub Pages

**Key Features:**
- Uses MkDocs Material theme for modern, responsive documentation
- Includes git revision dates for last-modified timestamps
- Minifies HTML output for better performance
- Supports both `master` and `main` as primary branches
- Strict building to catch errors early

**Required Repository Settings:**
1. Enable GitHub Pages in repository settings
2. Set Pages source to "GitHub Actions"
3. Ensure the repository has appropriate permissions for Pages deployment

**Directory Structure:**
```
src_docs/
├── mkdocs.yml          # MkDocs configuration
└── md/                 # Markdown documentation files
    ├── index.md        # Homepage with TOC
    ├── quickstart.md   # Quick start guide
    ├── installation.md # Installation instructions
    └── ...             # Additional documentation chapters

docs/                   # Built documentation output (generated)
└── .nojekyll          # Disable Jekyll processing
```

**Deployment URL:**
The documentation will be available at: `https://{username}.github.io/{repository-name}/`

## Adding This Workflow to Your Repository

To activate this workflow:

1. Copy the `_github` directory to `.github` in your repository root:
   ```bash
   cp -r _github .github
   ```

2. Commit and push the workflow files:
   ```bash
   git add .github/
   git commit -m "Add documentation build workflow"
   git push
   ```

3. Configure GitHub Pages in your repository settings:
   - Go to Settings → Pages
   - Set Source to "GitHub Actions"
   - The workflow will automatically run on the next push

## Customization

You can customize the workflow by modifying `docs.yml`:

- **Python version:** Change the `python-version` in the setup step
- **MkDocs plugins:** Add or remove plugins in the install step  
- **Build triggers:** Modify the `on:` section to change when the workflow runs
- **Branch names:** Update branch references if using different primary branch names

## Troubleshooting

**Common Issues:**

1. **Build fails with "No such file or directory":**
   - Ensure `src_docs/mkdocs.yml` exists and is properly configured
   - Check that all referenced markdown files exist in `src_docs/md/`

2. **Git revision dates not working:**
   - The workflow configures Git automatically, but ensure your repository has commit history
   - The plugin requires full git history (fetch-depth: 0)

3. **Pages deployment fails:**
   - Check that GitHub Pages is enabled in repository settings
   - Ensure the repository has necessary permissions for Pages deployment
   - Verify the workflow has `pages: write` and `id-token: write` permissions

4. **MkDocs build errors:**
   - Review the build logs for specific error messages
   - Test locally with `mkdocs serve` before committing
   - Ensure all internal links are valid

**Local Testing:**
```bash
cd src_docs
pip install mkdocs mkdocs-material mkdocs-git-revision-date-localized-plugin
mkdocs serve
```

This will start a local development server to preview the documentation.