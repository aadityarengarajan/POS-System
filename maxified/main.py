import functions.billing
import functions.reports
import functions.stock_management

menu = """
==========================================
SALES MANAGEMENT SYSTEM FOR STORES
==========================================

WHAT WOULD YOU LIKE TO DO?

(1) ADD NEW ITEM TO INVENTORY
(2) ADD NEW STOCK TO INVENTORY
(3) PERFORM BILLING FOR CUSTOMER
(4) VIEW CASH MEMO GIVEN CODE
(5) VIEW SALES REPORT(S)
(6) VIEW LIST OF AVAILABLE ITEMS
(7) GENERATE ORDER LIST FOR ITEMS WHERE STOCK < 20
(0) EXIT

YOUR CHOICE : """

report_menu = """
==========================================
VIEW SALES REPORT(S)
==========================================

WHAT TYPE OF SALES REPORT WOULD YOU LIKE TO VIEW?

(1) DAILY SALES REPORT
(2) MONTHLY SALES REPORT
(3) YEARLY SALES REPORT
(4) ITEM-WISE SALES REPORT
(0) BACK TO MAIN MENU

YOUR CHOICE : """

while True:
	while 1:
		try:
			ch = int(input(menu))
			break
		except:
			print("PLEASE ENTER A VALID INTEGER")
			continue
	if ch==1:
		functions.stock_management.add_item()
		print("\n"*2)
	elif ch==2:
		functions.stock_management.add_stock()
		print("\n"*2)
	elif ch==3:
		functions.billing.bill()
		print("\n"*2)
	elif ch==4:
		functions.reports.cash_memo()
		print("\n"*2)
	elif ch==5:
		while 1:
			try:
				ch = int(input(report_menu))
				break
			except:
				print("PLEASE ENTER A VALID INTEGER")
				continue
		if ch==1:
			functions.reports.daily_sales_report()
		elif ch==2:
			functions.reports.monthly_sales_report()
		elif ch==3:
			functions.reports.yearly_sales_report()
		elif ch==4:
			functions.reports.item_wise_report()
		print("\n"*2)
	elif ch==6:
		functions.reports.items_available()
		print("\n"*2)
	elif ch==7:
		functions.reports.order_stock_list()
		print("\n"*2)
	elif ch==0:
		break
