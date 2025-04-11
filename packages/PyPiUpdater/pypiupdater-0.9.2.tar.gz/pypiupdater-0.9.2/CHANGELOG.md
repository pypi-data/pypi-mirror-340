# Changelog

## 0.8-0.9: CI woodpecker (25.04.10-11)
- Changes to the pipeline no

## 0.7.x
### 0.7.2: Removed Debugging Leftovers
- Cleaned up code used for debugging.

### 0.7.1: Fixed Prerelease Update Detection
- Prevented prerelease versions from being listed as updates, as they must be installed manually.

### 0.7.0: Added Function to Install Packages
- Introduced the `install_package` function, allowing packages to be installed directly through the app.
  - Useful for optional dependencies that need to be installed separately. This enables installation via the UI.

---

## 0.6.x
### 0.6.1: Classifier
- Added Classifier for pypi

### 0.6.0: New Local Update Feature
- Added support for updating from a local folder containing package files.
  - Scans a specified folder for available updates.
  - Installs updates directly from local package files.
- **Note:** Local version handling depends on how dependencies are managed.
  - Example: If a package requires **PyPiUpdater 0.6.0**, but the installed version is **0.0.1** (e.g., from a dev environment), **OptimaLab35 v0.9.1** may not install correctly.
  - This is due to **pip's dependency checks**, ensuring all required versions are satisfied before installation.

---

## 0.5.0: Rework (BREAKING CHANGE)
- Improved code consistency: return values are now always **lists** when containing multiple objects.
- **Simplified the package**: Removed the default waiting period for update checks.
  - It is now the **developer's responsibility** to decide when to check for updates. A separate independent function may be introduced later.
  - The last update check is still saved in the config and returned as a `time.time()` object.

---

## 0.4.0: Rework (BREAKING CHANGE)
- The log file is now a JSON file, allowing it to store multiple package names, versions, and last update timestamps.
- Some return values are now lists.

---

## 0.3.0: Rework (BREAKING CHANGE)
- Changed how program behaves

---

## 0.2.1: CI/CD pipeline
- Added auto tagging and publishing

---

## 0.0.1: Project Initiation
- First working version
- ATM terminal promt to accept or deny update
- More to come soon
