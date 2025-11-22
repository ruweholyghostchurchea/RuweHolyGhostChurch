# Python Version Management Guide

## 🔴 CRITICAL: This Project Uses Python 3.12

This project **MUST** use Python 3.12. Using any other Python version (3.11, 3.10, etc.) will cause package import errors, especially with `psycopg2-binary` and `Pillow`.

---

## ✅ Current Configuration

- **Python Version**: 3.12
- **Module in .replit**: `python-3.12`
- **Package Manager**: Use `python3 -m pip` (NOT `pip` or `pip3` alone)
- **Database**: PostgreSQL (via `psycopg2-binary`)

---

## 🔧 How to Verify Your Python Version

```bash
python3 --version
# Should output: Python 3.12.x

which python3
# Should output: /nix/store/.../python3-3.12.x/bin/python3
```

---

## 📦 Installing Packages (The Right Way)

### ✅ CORRECT Method:
```bash
# Always use python3 -m pip to ensure correct Python version
python3 -m pip install -r requirements.txt

# For individual packages:
python3 -m pip install Django==5.2.4
```

### ❌ WRONG Methods:
```bash
# DON'T use these - they may use wrong Python version:
pip install -r requirements.txt        # ❌ Wrong!
pip3 install -r requirements.txt       # ❌ Wrong!
python -m pip install ...              # ❌ Wrong (python might be 2.x)
```

---

## 🚨 Common Errors & Solutions

### Error 1: "ModuleNotFoundError: No module named 'psycopg2._psycopg'"

**Cause**: `psycopg2-binary` was installed for wrong Python version

**Solution**:
```bash
python3 -m pip uninstall -y psycopg2-binary
python3 -m pip install psycopg2-binary==2.9.10 --force-reinstall --no-cache-dir
```

### Error 2: "Cannot use ImageField because Pillow is not installed"

**Cause**: `Pillow` was installed for wrong Python version

**Solution**:
```bash
python3 -m pip install Pillow==11.3.0 --force-reinstall --no-cache-dir
```

### Error 3: "ImportError: Couldn't import Django"

**Cause**: Packages installed for wrong Python version

**Solution**:
```bash
# Reinstall everything for correct Python version
python3 -m pip install -r requirements.txt --force-reinstall
```

---

## 🔄 Changing Python Version (Advanced)

If you **must** change the Python version (not recommended), follow these steps:

### Step 1: Update Module Configuration
```bash
# Remove old Python module (use Replit module tools)
# Install new Python module (e.g., python-3.13)
```

### Step 2: Update Configuration Files
- [ ] Update `.python-version` file
- [ ] Update this guide (PYTHON_VERSION_GUIDE.md)
- [ ] Update `replit.md` documentation

### Step 3: Reinstall ALL Packages
```bash
# Clear old packages
python3 -m pip freeze | xargs python3 -m pip uninstall -y

# Reinstall fresh
python3 -m pip install -r requirements.txt --force-reinstall --no-cache-dir
```

### Step 4: Test Critical Dependencies
```bash
# Test psycopg2
python3 -c "import psycopg2; print('✅ psycopg2 works')"

# Test Pillow
python3 -c "from PIL import Image; print('✅ Pillow works')"

# Test Django
python3 -c "import django; print('✅ Django works')"
```

### Step 5: Run Migrations & Test Server
```bash
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:5000
```

---

## 📋 Version Lock Files

The following files lock the Python version:

1. **`.python-version`** - Contains: `3.12`
2. **`.replit`** - Contains: `modules = ["python-3.12"]`
3. **`requirements.txt`** - Comments specify Python 3.12
4. **`replit.md`** - Documentation specifies Python 3.12

**IMPORTANT**: Keep all these files synchronized!

---

## 🎯 Quick Troubleshooting Checklist

If packages aren't working:

- [ ] Check Python version: `python3 --version` → Should be 3.12.x
- [ ] Check .replit file has `python-3.12` module
- [ ] Reinstall problematic package with `--force-reinstall`
- [ ] Always use `python3 -m pip` (never just `pip`)
- [ ] Restart the workflow after package changes
- [ ] Check logs for specific import errors

---

## 📞 Need Help?

If you continue having Python version conflicts:

1. Check this guide's troubleshooting section
2. Verify all version lock files are consistent
3. Consider creating a fresh environment
4. Review the error logs carefully for version mismatches

---

**Last Updated**: November 22, 2025  
**Python Version**: 3.12  
**Django Version**: 5.2.4
