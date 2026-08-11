const { test, expect } = require('@playwright/test');
const path = require('path');

const fixture = name => 'file://' + path.resolve(__dirname, name + '.html');

test('sup does not expand the line box', async ({ page }) => {
    await page.goto(fixture('sup-line-height'));
    const lineHeight = await page.$eval('sup', el => getComputedStyle(el).lineHeight);
    expect(lineHeight).toBe('0px');
});
