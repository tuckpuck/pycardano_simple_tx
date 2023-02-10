from pycardano import PaymentSigningKey, StakeSigningKey, PaymentVerificationKey, StakeVerificationKey, Address, Network, TransactionBuilder, TransactionOutput, BlockFrostChainContext
import time
from blockfrost import BlockFrostApi, ApiError, ApiUrls
import config

# Generate payment signing key
payment_signing_key = PaymentSigningKey.generate()
# Generate payment verification key
payment_verification_key = PaymentVerificationKey.from_signing_key(payment_signing_key)
# save payment signing key as a file
payment_signing_key.save("payment.skey")
# save payment verification key as a file
payment_verification_key.save("payment.vkey")

# Generate stake signing key
stake_signing_key = StakeSigningKey.generate()
# Generate stake verification key
stake_verification_key = StakeVerificationKey.from_signing_key(stake_signing_key)
# save stake signing key as a file
stake_signing_key.save("stake.skey")
# save stake verification key as a file
stake_verification_key.save("stake.vkey")

# Build first address
address1 = Address(
    payment_verification_key.hash(), 
    stake_verification_key.hash(), 
    Network.TESTNET
    )
# Save address as file
file = open('address.addr', 'w')
file.write(str(address1))
file.close()

# Take a pause to allow person running this script to fund wallet via faucet
print("You have 2 minutes to fund the wallet at " + str(address1) + " using https://docs.cardano.org/cardano-testnet/tools/faucet. Use the preview network.")
time.sleep(120)

# Set up API URL with API key
api = BlockFrostApi(project_id=config.blockfrost_api_key, base_url=ApiUrls.preview.value)

try:
    # Check that URL connection is working
    health = api.health()
    print(health)
    # Check the UTXOs at an address
    address = api.address_utxos(
        address=address1)
    print(address)
    # Print tx hashes of the UTXOs
    for amount in address:
        print(amount.tx_hash)
    # Print error if something goes wrong
except ApiError as e:
    print(e)


# Generate second payment signing key
payment_signing_key_2 = PaymentSigningKey.generate()
# Generate second payment verification key
payment_verification_key_2 = PaymentVerificationKey.from_signing_key(payment_signing_key_2)
# save second payment signing key as a file
payment_signing_key_2.save("payment2.skey")
# save second payment verification key as a file
payment_verification_key_2.save("payment2.vkey")

# Generate second stake signing key
stake_signing_key_2 = StakeSigningKey.generate()
# Generate second stake verification key
stake_verification_key_2 = StakeVerificationKey.from_signing_key(stake_signing_key_2)
# save second stake signing key as a file
stake_signing_key_2.save("stake2.skey")
# save second stake verification key as a file
stake_verification_key_2.save("stake2.vkey")

# Build second address
address2 = Address(
    payment_verification_key_2.hash(), 
    stake_verification_key_2.hash(), 
    Network.TESTNET
    )
# Save address as file
file = open('address2.addr', 'w')
file.write(str(address2))
file.close()

# Set network
network = Network.TESTNET
# Prepare blockfrost API wrapper
context = BlockFrostChainContext(config.blockfrost_api_key, network, base_url=ApiUrls.preview.value)

# Define where the tx is going from/to
address_from = str(address1)
sk_path = 'payment.skey'
address_to = str(address2)

# Build the tx
tx_builder = TransactionBuilder(context)
tx_builder.add_input_address(address_from)
tx_builder.add_output(TransactionOutput.from_primitive([address_to, 5000000]))
payment_signing_key = PaymentSigningKey.load(sk_path)

# Sign and submit
signed_tx = tx_builder.build_and_sign([payment_signing_key], change_address=Address.from_primitive(address_from)) 
context.submit_tx(signed_tx.to_cbor())
# You can check if the tx went through by inputting address2 into https://preview.cexplorer.io/