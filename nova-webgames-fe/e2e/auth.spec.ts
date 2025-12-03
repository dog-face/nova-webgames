import { test, expect } from './fixtures';

test.describe('Authentication Flow', () => {
  test('should sign up a new user', async ({ page }) => {
    const timestamp = Date.now();
    const random = Math.floor(Math.random() * 10000);
    const username = `u${timestamp}${random}`.slice(0, 20); // Max 20 chars
    const email = `test_${timestamp}_${random}@example.com`;
    const password = 'TestPassword123!';

    await page.goto('/signup');

    // Fill in signup form
    await page.fill('input[id="username"]', username);
    await page.fill('input[id="email"]', email);
    await page.fill('input[id="password"]', password);

    // Wait for signup API call
    const signupResponse = page.waitForResponse(
      response => response.url().includes('/auth/signup'),
      { timeout: 15000 }
    );
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Wait for API response
    const response = await signupResponse;
    
    // Check if signup was successful (201 = Created is success for signup)
    if (response.status() !== 201 && response.status() !== 200) {
      const errorText = await page.locator('.error-message, [class*="error"]').textContent({ timeout: 2000 }).catch(() => 'Unknown error');
      throw new Error(`Signup failed with status ${response.status()}. Error: ${errorText}`);
    }

    // Should redirect to home page after successful signup
    await page.waitForURL('/', { timeout: 15000 });
    
    // Should see welcome message with username (use first() to avoid strict mode violation)
    await expect(page.locator(`text=${username}`).first()).toBeVisible({ timeout: 10000 });
  });

  test('should show error for duplicate email', async ({ page }) => {
    const timestamp = Date.now();
    const random = Math.floor(Math.random() * 10000);
    const shortUsername1 = `u${timestamp}${random}`.slice(0, 20);
    const shortUsername2 = `u${timestamp}${random + 1}`.slice(0, 20);
    const email = `duplicate_${timestamp}_${random}@example.com`;
    const password = 'TestPassword123!';

    // Sign up first user
    await page.goto('/signup');
    await page.fill('input[id="username"]', shortUsername1);
    await page.fill('input[id="email"]', email);
    await page.fill('input[id="password"]', password);
    
    // Wait for signup API call
    const signupResponse1 = page.waitForResponse(
      response => response.url().includes('/auth/signup'),
      { timeout: 15000 }
    );
    
    await page.click('button[type="submit"]');
    
    // Wait for API response
    const response1 = await signupResponse1;
    if (response1.status() !== 201 && response1.status() !== 200) {
      throw new Error(`First signup failed with status ${response1.status()}`);
    }
    
    await page.waitForURL('/', { timeout: 10000 });

    // Logout
    await page.click('button:has-text("Logout")');
    await page.waitForURL('/login', { timeout: 10000 });

    // Try to sign up with same email
    await page.goto('/signup');
    await page.fill('input[id="username"]', shortUsername2);
    await page.fill('input[id="email"]', email);
    await page.fill('input[id="password"]', password);
    await page.click('button[type="submit"]');

    // Should show error message
    await expect(page.locator('.error-message')).toBeVisible({ timeout: 5000 });
  });

  test('should login with valid credentials', async ({ page }) => {
    const timestamp = Date.now();
    const random = Math.floor(Math.random() * 10000);
    const username = `u${timestamp}${random}`.slice(0, 20); // Max 20 chars
    const email = `login_${timestamp}_${random}@example.com`;
    const password = 'TestPassword123!';

    // First sign up
    await page.goto('/signup');
    await page.fill('input[id="username"]', username);
    await page.fill('input[id="email"]', email);
    await page.fill('input[id="password"]', password);
    await page.click('button[type="submit"]');
    await page.waitForURL('/', { timeout: 10000 });

    // Logout
    await page.click('button:has-text("Logout")');
    await page.waitForURL('/login', { timeout: 10000 });

    // Login
    await page.fill('input[id="username"]', username);
    await page.fill('input[id="password"]', password);
    await page.click('button[type="submit"]');

    // Should redirect to home
    await page.waitForURL('/', { timeout: 10000 });
    await expect(page.locator(`text=${username}`).first()).toBeVisible();
  });

  test('should show error for invalid login credentials', async ({ page }) => {
    await page.goto('/login');

    await page.fill('input[id="username"]', 'nonexistent_user');
    await page.fill('input[id="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');

    // Should show error message
    await expect(page.locator('.error-message')).toBeVisible({ timeout: 5000 });
  });

  test('should logout successfully', async ({ authenticatedUser, page }) => {
    // User is already authenticated via fixture
    await page.goto('/');

    // Verify user is logged in (use first() to avoid strict mode violation)
    await expect(page.locator(`text=${authenticatedUser.username}`).first()).toBeVisible();

    // Click logout
    await page.click('button:has-text("Logout")');

    // Should redirect to login page
    await page.waitForURL('/login', { timeout: 15000 });
    
    // Wait for page to be fully loaded
    await page.waitForLoadState('networkidle');

    // Should not see user-specific content (use heading to avoid strict mode violation)
    await expect(page.locator('h2:has-text("Login")')).toBeVisible({ timeout: 10000 });
  });

  test('should protect routes when not authenticated', async ({ page }) => {
    // Clear any existing auth safely
    try {
      await page.evaluate(() => {
        if (window.location.origin === window.location.origin) {
          localStorage.clear();
        }
      });
    } catch (e) {
      // Ignore localStorage errors
    }

    // Try to access protected route
    await page.goto('/game');

    // Should redirect to login
    await page.waitForURL('/login', { timeout: 10000 });

    // Try another protected route
    await page.goto('/leaderboard');
    await page.waitForURL('/login', { timeout: 10000 });

    await page.goto('/watch');
    await page.waitForURL('/login', { timeout: 10000 });
  });
});

