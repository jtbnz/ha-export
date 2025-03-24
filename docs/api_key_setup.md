# Setting Up Home Assistant API Access

This document explains how to create a Long-Lived Access Token in Home Assistant for API access.

## Creating a Long-Lived Access Token

1. **Log in to your Home Assistant instance** using your regular username and password.

2. **Navigate to your profile**:
   - Click on your username in the bottom-left corner of the Home Assistant interface.
   - This will take you to your user profile page.

3. **Scroll down to the "Long-Lived Access Tokens" section** at the bottom of your profile page.

4. **Create a new token**:
   - Click on the "Create Token" button.
   - Enter a name for your token (e.g., "Sensor Data Export").
   - Click "OK" to generate the token.

5. **Copy your token**:
   - A dialog will appear showing your newly created token.
   - **IMPORTANT**: Copy this token immediately and store it securely. For security reasons, Home Assistant will only show this token once.

6. **Use the token in your configuration**:
   - Copy the `secrets_template.py` file to `secrets.py`.
   - Replace the placeholder value for `HA_TOKEN` with your newly created token.
   - Update the `HA_URL` with your Home Assistant instance URL.

## Security Considerations

- Keep your token secure. Anyone with this token can access your Home Assistant instance.
- Use a dedicated token for each application or script.
- If you suspect a token has been compromised, you can delete it from your profile page and create a new one.
- The `secrets.py` file is included in `.gitignore` to prevent accidentally committing your token to version control.

## Token Permissions

By default, a Long-Lived Access Token has the same permissions as your user account. If you're concerned about security, consider:

1. Creating a dedicated user with limited permissions for API access.
2. Generate the token from this limited user account instead of your admin account.

## Troubleshooting

If you encounter authentication errors:

1. Verify that your token is correctly copied without any extra spaces.
2. Check that your Home Assistant URL is correct and accessible.
3. Ensure your Home Assistant instance is running and reachable from the machine running the script.
4. Verify that your user account has the necessary permissions to access the sensors you're trying to query.
