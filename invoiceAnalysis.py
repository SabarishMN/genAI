import pandas as pd
import json
import numpy as np
from getpass import getpass
from openai import OpenAI
import time
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SimpleField, SearchFieldDataType, SearchIndex
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

import utils

load_dotenv()
rec_endpoint = os.getenv("RECOGNIZER_ENDPOINT")
rec_key = os.getenv("RECOGNIZER_KEY")

document_analysis_client = DocumentAnalysisClient(
    endpoint=rec_endpoint, credential=AzureKeyCredential(rec_key)
)

def startAnalysis():
    form_urls = os.listdir("documents_invoice")
    print(form_urls)
    # id , entity_id , content , content_vector
    for index, url in enumerate(form_urls, 1):
        data = {}
        with open("documents_invoice/" + url, "rb") as file:
            poller = document_analysis_client.begin_analyze_document("prebuilt-invoice", file)
            invoices = poller.result()
            for idx1, invoice in enumerate(invoices.documents):
                print("--------Recognizing invoice #{}--------".format(index))
                invoice_id = invoice.fields.get("InvoiceId")
                if invoice_id:
                    print(f"Invoice Id: {invoice_id.value} has confidence: {invoice_id.confidence}")
                    data["invoice_id"] = invoice_id.value

                vendor_name = invoice.fields.get("VendorName")
                if vendor_name:
                    print(f"Vendor Name: {vendor_name.value} has confidence: {vendor_name.confidence}")
                    data["vendor_name"] = vendor_name.value

                vendor_address = invoice.fields.get("VendorAddress")
                if vendor_address:
                    print(f"Vendor Address: {vendor_address.value} has confidence: {vendor_address.confidence}")
                    data["vendor_address"] = vendor_address.value

                vendor_address_recipient = invoice.fields.get("VendorAddressRecipient")
                if vendor_address_recipient:
                    print(
                        f"Vendor Address Recipient: {vendor_address_recipient.value} has confidence: {vendor_address_recipient.confidence}")
                    data["vendor_address_recipient"] = vendor_address_recipient.value

                customer_name = invoice.fields.get("CustomerName")
                if customer_name:
                    print(f"Customer Name: {customer_name.value} has confidence: {customer_name.confidence}")
                    data["customer_name"] = customer_name.value

                customer_id = invoice.fields.get("CustomerId")
                if customer_id:
                    print(f"Customer Id: {customer_id.value} has confidence: {customer_id.confidence}")
                    data["customer_id"] = customer_id.value

                customer_address = invoice.fields.get("CustomerAddress")
                if customer_address:
                    print(f"Customer Address: {customer_address.value} has confidence: {customer_address.confidence}")
                    data["customer_address"] = customer_address.value

                customer_address_recipient = invoice.fields.get("CustomerAddressRecipient")
                if customer_address_recipient:
                    print(
                        f"Customer Address Recipient: {customer_address_recipient.value} has confidence: {customer_address_recipient.confidence}")
                    data["customer_address_recipient"] = customer_address_recipient.value

                invoice_date = invoice.fields.get("InvoiceDate")
                if invoice_date:
                    print(f"Invoice Date: {invoice_date.value} has confidence: {invoice_date.confidence}")
                    data["invoice_date"] = invoice_date.value

                invoice_total = invoice.fields.get("InvoiceTotal")
                if invoice_total:
                    print(f"Invoice Total: {invoice_total.value} has confidence: {invoice_total.confidence}")
                    data["invoice_total"] = invoice_total.value

                due_date = invoice.fields.get("DueDate")
                if due_date:
                    print(f"Due Date: {due_date.value} has confidence: {due_date.confidence}")
                    data["due_date"] = due_date.value

                purchase_order = invoice.fields.get("PurchaseOrder")
                if purchase_order:
                    print(f"Purchase Order: {purchase_order.value} has confidence: {purchase_order.confidence}")
                    data["purchase_order"] = purchase_order.value

                billing_address = invoice.fields.get("BillingAddress")
                if billing_address:
                    print(f"Billing Address: {billing_address.value} has confidence: {billing_address.confidence}")
                    data["billing_address"] = billing_address.value

                billing_address_recipient = invoice.fields.get("BillingAddressRecipient")
                if billing_address_recipient:
                    print(
                        f"Billing Address Recipient: {billing_address_recipient.value} has confidence: {billing_address_recipient.confidence}")
                    data["billing_address_recipient"] = billing_address_recipient.value

                shipping_address = invoice.fields.get("ShippingAddress")
                if shipping_address:
                    print(f"Shipping Address: {shipping_address.value} has confidence: {shipping_address.confidence}")
                    data["shipping_address"] = shipping_address.value

                shipping_address_recipient = invoice.fields.get("ShippingAddressRecipient")
                if shipping_address_recipient:
                    print(
                        f"Shipping Address Recipient: {shipping_address_recipient.value} has confidence: {shipping_address_recipient.confidence}")
                    data["shipping_address_recipient"] = shipping_address_recipient.value

                # Handle invoice items
                invoice_items = []
                for idx, item in enumerate(invoice.fields.get("Items").value):
                    item_data = {}
                    print(f"...Item #{idx + 1}")
                    item_description = item.value.get("Description")
                    if item_description:
                        print(
                            f"......Description: {item_description.value} has confidence: {item_description.confidence}")
                        item_data["description"] = item_description.value

                    item_quantity = item.value.get("Quantity")
                    if item_quantity:
                        print(f"......Quantity: {item_quantity.value} has confidence: {item_quantity.confidence}")
                        item_data["quantity"] = item_quantity.value

                    unit = item.value.get("Unit")
                    if unit:
                        print(f"......Unit: {unit.value} has confidence: {unit.confidence}")
                        item_data["unit"] = unit.value

                    unit_price = item.value.get("UnitPrice")
                    if unit_price:
                        print(f"......Unit Price: {unit_price.value} has confidence: {unit_price.confidence}")
                        item_data["unit_price"] = unit_price.value

                    product_code = item.value.get("ProductCode")
                    if product_code:
                        print(f"......Product Code: {product_code.value} has confidence: {product_code.confidence}")
                        item_data["product_code"] = product_code.value

                    item_date = item.value.get("Date")
                    if item_date:
                        print(f"......Date: {item_date.value} has confidence: {item_date.confidence}")
                        item_data["date"] = item_date.value

                    tax = item.value.get("Tax")
                    if tax:
                        print(f"......Tax: {tax.value} has confidence: {tax.confidence}")
                        item_data["tax"] = tax.value

                    amount = item.value.get("Amount")
                    if amount:
                        print(f"......Amount: {amount.value} has confidence: {amount.confidence}")
                        item_data["amount"] = amount.value

                    # Add the item data to the invoice items list
                    invoice_items.append(item_data)

                # Add the invoice items to the main data dictionary
                data["items"] = invoice_items

                # Add any remaining fields
                subtotal = invoice.fields.get("SubTotal")
                if subtotal:
                    print(f"Subtotal: {subtotal.value} has confidence: {subtotal.confidence}")
                    data["subtotal"] = subtotal.value

                total_tax = invoice.fields.get("TotalTax")
                if total_tax:
                    print(f"Total Tax: {total_tax.value} has confidence: {total_tax.confidence}")
                    data["total_tax"] = total_tax.value

                previous_unpaid_balance = invoice.fields.get("PreviousUnpaidBalance")
                if previous_unpaid_balance:
                    print(
                        f"Previous Unpaid Balance: {previous_unpaid_balance.value} has confidence: {previous_unpaid_balance.confidence}")
                    data["previous_unpaid_balance"] = previous_unpaid_balance.value

                amount_due = invoice.fields.get("AmountDue")
                if amount_due:
                    print(f"Amount Due: {amount_due.value} has confidence: {amount_due.confidence}")
                    data["amount_due"] = amount_due.value

                service_start_date = invoice.fields.get("ServiceStartDate")
                if service_start_date:
                    print(
                        f"Service Start Date: {service_start_date.value} has confidence: {service_start_date.confidence}")
                    data["service_start_date"] = service_start_date.value

                service_end_date = invoice.fields.get("ServiceEndDate")
                if service_end_date:
                    print(f"Service End Date: {service_end_date.value} has confidence: {service_end_date.confidence}")
                    data["service_end_date"] = service_end_date.value

                service_address = invoice.fields.get("ServiceAddress")
                if service_address:
                    print(f"Service Address: {service_address.value} has confidence: {service_address.confidence}")
                    data["service_address"] = service_address.value

                service_address_recipient = invoice.fields.get("ServiceAddressRecipient")
                if service_address_recipient:
                    print(
                        f"Service Address Recipient: {service_address_recipient.value} has confidence: {service_address_recipient.confidence}")
                    data["service_address_recipient"] = service_address_recipient.value

                remittance_address = invoice.fields.get("RemittanceAddress")
                if remittance_address:
                    print(
                        f"Remittance Address: {remittance_address.value} has confidence: {remittance_address.confidence}")
                    data["remittance_address"] = remittance_address.value

                remittance_address_recipient = invoice.fields.get("RemittanceAddressRecipient")
                if remittance_address_recipient:
                    print(
                        f"Remittance Address Recipient: {remittance_address_recipient.value} has confidence: {remittance_address_recipient.confidence}")
                    data["remittance_address_recipient"] = remittance_address_recipient.value

                print("----------------------------------------")
            blob_data = dict(id=index, invoice_id=data["invoice_id"], content=str(data),
                             content_vector=utils.get_embedding(str(data)))
            # print(blob_data)
            with open(url[:-4]+"-data.json", 'w') as json_file:
                json.dump(blob_data, json_file, indent=4)
            utils.writeToBlob(url[:-4]+"-data.json")

def startTask():
    utils.aiSearch(index_name="invoice_index", top_k=2)

startTask()