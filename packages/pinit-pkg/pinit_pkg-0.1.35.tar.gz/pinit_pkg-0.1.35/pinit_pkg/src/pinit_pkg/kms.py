import boto3
import json
import jwt

from datetime import datetime, timedelta, UTC
from loguru import logger

from .decorators.execution_time import execution_time


kms_client = boto3.client('kms')

@execution_time
def kms_new_key(alias: str) -> str:
    """Create a new asymmetric KMS key for digital signatures.

    Args:
        alias (str): The alias name for the key. Will be prefixed with 'alias/'.

    Returns:
        str: The key ID of the created KMS key
    """
    try:
        response = kms_client.create_key(
            Description=f'Asymmetric signing key for {alias}',
            KeyUsage='SIGN_VERIFY',
            CustomerMasterKeySpec='RSA_4096',
            Origin='AWS_KMS',
            Tags=[{
                'TagKey': 'Purpose',
                'TagValue': 'DigitalSignature'
            }]
        )

        key_id = response['KeyMetadata']['KeyId']

        kms_client.create_alias(
            AliasName=f'alias/{alias}',
            TargetKeyId=key_id
        )

        return key_id
    except Exception as e:
        logger.error(f"Error creating KMS key with alias {alias}: {e}")
        raise


@execution_time
def kms_sign_payload(payload: dict, key_id: str, expiration_minutes: int = 60) -> str:
    """Generate a JWT token using KMS to sign the payload.

    Args:
        payload (dict): The payload to include in the JWT
        key_id (str): The KMS key ID to use for signing
        expiration_minutes (int, optional): Token expiration time in minutes. Defaults to 60.

    Returns:
        str: The signed JWT token
    """
    try:
        now = datetime.now(UTC)
        payload['iat'] = str(now)

        if expiration_minutes > 0:
            payload['exp'] = str(now + timedelta(minutes=expiration_minutes))

        header = {
            'typ': 'JWT',
            'alg': 'RS256',
            'kid': key_id
        }

        header_encoded = jwt.utils.base64url_encode(json.dumps(header).encode('utf-8')).decode('utf-8')
        payload_encoded = jwt.utils.base64url_encode(json.dumps(payload).encode('utf-8')).decode('utf-8')

        message = f"{header_encoded}.{payload_encoded}"

        signature = kms_client.sign(
            KeyId=key_id,
            Message=message.encode('utf-8'),
            MessageType='RAW',
            SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA_256'
        )['Signature']

        signature_encoded = jwt.utils.base64url_encode(signature).decode('utf-8')
        token = f"{message}.{signature_encoded}"

        return token

    except Exception as e:
        logger.error(f"Error signing payload with KMS: {e}")
        raise


@execution_time
def kms_verify_signature(token: str, key_id: str) -> bool:
    """Verify a JWT token signature using AWS KMS.

    Args:
        token (str): The JWT token to verify
        key_id (str): The KMS key ID used to sign the token

    Returns:
        bool: True if signature is valid, False otherwise
    """
    logger.info(f"Verifying signature for token: {token}")
    logger.info(f"Key ID: {key_id}")
    try:
        header_encoded, payload_encoded, signature_encoded = token.split('.')
        message = f"{header_encoded}.{payload_encoded}"
        signature = jwt.utils.base64url_decode(signature_encoded)

        response = kms_client.verify(
            KeyId=key_id,
            Message=message.encode('utf-8'),
            MessageType='RAW',
            Signature=signature,
            SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA_256'
        )

        return response['SignatureValid']

    except Exception as e:
        logger.error(f"Error verifying signature with KMS: {e}")
        return False
