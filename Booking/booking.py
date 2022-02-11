import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import Booking.constants as const
from prettytable import PrettyTable
from time import sleep





class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\SeleniumDriver\chromedriver_win32",teardown=False):

        self.driver_path = driver_path

        self.teardown = teardown

        os.environ['PATH'] += self.driver_path

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])        

        super(Booking, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()


    def __exit__(self, exc_type, exc_vlue, exc_tb):
        if self.teardown:
            self.quit()
    
    def land_first_page(self):

        self.get(const.BASE_URL)

    
    def element_exists_by_id(self, id):

        try:
            self.find_element_by_id(id)
        except NoSuchElementException:
            return False
        return True

    
    def fill_details(self):

        departure_city_searchbox = self.find_element_by_id('FromSector_show')
        departure_city_searchbox.clear()
        departure_city_searchbox.send_keys(const.FROM)
        
        departure_lists = self.find_element_by_id('ui-id-1')
        departure_list_options = departure_lists.find_elements_by_class_name('ui-menu-item')

        for option in departure_list_options:

            city = str(option.find_element_by_class_name('ct').get_attribute('innerHTML'))
            if const.FROM_CODE in city:

                option.click()
                break
        
        sleep(1)

        arrival_city_searchbox = self.find_element_by_id('Editbox13_show')
        arrival_city_searchbox.clear()
        arrival_city_searchbox.send_keys(const.TO)
        
        arrival_lists = self.find_element_by_id('ui-id-2')
        arrival_list_options = arrival_lists.find_elements_by_class_name('ui-menu-item')
        

        for temp in arrival_list_options:

            arrival_city = str(temp.find_element_by_class_name('ct').get_attribute('innerHTML')).strip()

            if const.TO_CODE in arrival_city:
            
                temp.click()
                break
        

        travel_date_field = self.find_element_by_css_selector(
            f'li[id$="{const.DATE}"]'
        ) 

        travel_date_field.click()
           
        
        passengers_count = self.find_element_by_css_selector(
            'a[class="dropbtn_n9"]'
        )

        passengers_count.click()

        for i in range(1,const.ADULTS):

            plus_button_element = self.find_element_by_css_selector(
                'input[class="plus_box1"]'
            )
        
            plus_button_element.click()
        

        for i in range(const.CHILD):

            child_plus_button_element = self.find_element_by_css_selector(
                'input[class="plus_boxChd"]'
            )

            child_plus_button_element.click()
        

        done_element = self.find_element_by_id('traveLer')
        done_element.click()
    
        class_element = self.find_element_by_css_selector(
            'a[class="dropbtn_n10"]'
        )

        class_element.click()

        
        # premium_economy_class  = self.find_element_by_css_selector(
        #     'input[value="4"]'
        # )
        # premium_economy_class.click()


        # class_done_element = self.find_element_by_id('tripType')
        # class_done_element.click()
        

        check_student_box_element = self.find_element_by_id('chkStudent')
        check_student_box_element.click()


        search_button_element = self.find_element_by_css_selector(
            'input[value="Search"]'
        )

        search_button_element.click()
    

    def apply_filter(self):

        # morning_departure_filter = self.find_element_by_css_selector(
        #     'div[ng-click="TimeFilterDEP(3,12,18);"]'
        # )

        # morning_departure_filter.click()


        non_stop_filter = self.find_element_by_id('divchkOneStop')

        non_stop_filter.click()
    

    def select_cheapest_flight(self):

        total_flight_lists_element = self.find_element_by_css_selector(
            'div[data-infinite-scroll="loadMoreOutBound()"]'
        )

        total_flights_element = total_flight_lists_element.find_elements_by_css_selector(
            'div[data-ng-repeat^="(segID,s)"]'
        )


        cheapest_flight_element = total_flights_element[0]

        book_button = cheapest_flight_element.find_element_by_css_selector(
            'button[ng-click="SelectedFlight_L(s)"]'
        )

        book_button.click()

        if const.INSURANCE == 'NO':

            no_insurance_added = self.find_element_by_id('notinsure')
            no_insurance_added.click()
        
        else:

            add_insurance = self.find_element_by_id('chkInsurance')
            add_insurance.click()
        

        email_field = self.find_element_by_id('txtEmailId')
        email_field.clear()
        email_field.send_keys(const.EMAIL)

        sleep(1)

        verify_email = self.find_element_by_id('divContinueReview2')
        verify_email.click()
    

    def add_travellers_details(self):
        
        count = 0

        for adult in const.ADULTS_DETAILS:


            if count > 0 :

                

                add_adult_element = self.find_element_by_css_selector(
                    'a[class="add_adlt"]'
                )

                add_adult_element.click()

                


            adult_title_box = self.find_element_by_id(f'titleAdult{count}')

            

            if adult[0] == 'MR':

                adult_title_MR = adult_title_box.find_element_by_css_selector(
                    'option[value="Mr"]'
                )

                adult_title_MR.click()
            
            elif adult[0] == 'MS':

                adult_title_MS = adult_title_box.find_element_by_css_selector(
                    'option[value="Ms"]'
                )

                adult_title_MS.click()
            
            else:

                adult_title_Mrs = adult_title_box.find_element_by_css_selector(
                    'option[value="Mrs"]'
                )

                adult_title_Mrs.click()
            

            first_name_element = self.find_element_by_id(f'txtFNAdult{count}')
            first_name_element.clear()
            first_name_element.send_keys(adult[1])

            sleep(1)

            last_name_element = self.find_element_by_id(f'txtLNAdult{count}')
            last_name_element.clear()
            last_name_element.send_keys(adult[2])

            if self.element_exists_by_id(f'txtDocumentIdAdult{count}'):

                text_doc_element = self.find_element_by_id(f'txtDocumentIdAdult{count}')
                text_doc_element.clear()
                text_doc_element.send_keys(adult[3])

            count = count + 1




        #Child Part

        if const.CHILD > 0 :

            children_count = 0

            for child in const.CHILD_DETAILS:

                if children_count > 0 :

                    add_child_element = self.find_element_by_css_selector(
                        'a[ng-if="NoChd >0"]'
                    )

                    add_child_element.click()


                child_title_box = self.find_element_by_id(f'titleChild{children_count}')

                if child[0] == 'Master':

                    child_title_option  = child_title_box.find_element_by_css_selector(
                        'option[value="MSTR"]'
                    )

                    child_title_option.click()
                
                else:

                    child_title_option  = child_title_box.find_element_by_css_selector(
                        'option[value="Miss"]'
                    )

                    child_title_option.click()


                child_first_name_element = self.find_element_by_id(f'txtFNChild{children_count}')
                child_first_name_element.clear()
                child_first_name_element.send_keys(child[1])

                sleep(1)

                child_last_name_element = self.find_element_by_id(f'txtLNChild{children_count}')
                child_last_name_element.clear()
                child_last_name_element.send_keys(child[2])



                children_count = children_count + 1

        

        
    

    def confirm_booking(self):

        #Mobile Phone

        mobile_field_element = self.find_element_by_id('txtCPhone')
        mobile_field_element.clear()
        mobile_field_element.send_keys(const.MOBILE)



        confirm_book_element = self.find_element_by_id('spnTransaction')
        confirm_book_element.click()
    



    def make_payment(self):

        card_number_field = self.find_element_by_id('CC')
        card_number_field.clear()
        card_number_field.send_keys(const.CARD_NO)


        card_holder_name_field = self.find_element_by_id('CCN')
        card_holder_name_field.clear()
        card_holder_name_field.send_keys(const.HOLDER_NAME)


        month_field = self.find_element_by_id('CCMM')
        month_option_element = month_field.find_element_by_css_selector(
            f'option[value="{const.MONTH}"]'
        )
        month_option_element.click()


        year_field = self.find_element_by_id('CCYYYY')
        year_option_element = year_field.find_element_by_css_selector(
            f'option[value="{const.YEAR}"]'
        )
        year_option_element.click()


    def print_details(self, table):

        print()

        print('-------------------------------------------------------------------------------------------')

        print('                     ➤ ➤ ➤  Flight Booking bot  ➤ ➤ ➤                       ')

        print('-------------------------------------------------------------------------------------------')

        print()

        print('                             ✦ Ticket Itinerary ✦                                             ')

        print()

        print(table)

        total_price_element = self.find_element_by_id('spnGrndTotal')
        total_price = str(total_price_element.get_attribute('innerHTML')).strip()

        print()
        print(f'★ Grand Total(Tax inclusive) : {total_price}')
        print()
        print('❝ Please Make the payment to confirm your booking ❞')



    def print_ticket_summary(self):

        total_flights_in_journey = self.find_elements_by_css_selector(
            'div[data-ng-repeat="(bID,b) in j.segs[0].bonds"]'
        )

        

        flight_details_box = total_flights_in_journey[1]

        flights_in_journey = flight_details_box.find_elements_by_css_selector(
            'div[data-ng-repeat^="(lID,l)"]'
        )

        

        flights_details = []

        for single_flight in flights_in_journey:

            flight_name_element = single_flight.find_element_by_css_selector(
                'span[ng-bind="l.airName"]'
            )

            flight_name = str(flight_name_element.get_attribute('innerHTML')).strip()


            flight_number_element = single_flight.find_element_by_css_selector(
                'span[ng-bind^="l.airCode"]'
            )

            flight_number = str(flight_number_element.get_attribute('innerHTML')).strip()

            departure_time_element = single_flight.find_element_by_css_selector(
                'strong[ng-bind="l.depTM"]'
            )

            departure_time = str(departure_time_element.get_attribute('innerHTML')).strip()

            departure_city_and_code_element = single_flight.find_elements_by_css_selector(
                'span[ng-bind^="l.org"]'
            )

            

            departure_city_element = departure_city_and_code_element[0]

            departure_city = str(departure_city_element.get_attribute('innerHTML')).strip()

            departure_city_code_element = departure_city_and_code_element[1]

            departure_city_code = str(departure_city_code_element.get_attribute('innerHTML')).strip()

            

            departure_date_element = single_flight.find_element_by_css_selector(
                'span[ng-bind="l.depDT"]'
            )
            
            departure_date = str(departure_date_element.get_attribute('innerHTML')).strip()

            arrival_time_element = single_flight.find_element_by_css_selector(
                'strong[ng-bind="l.arrTM"]'
            )

            arrival_time = str(arrival_time_element.get_attribute('innerHTML')).strip()

            arrival_city_and_code_element = single_flight.find_elements_by_css_selector(
                'span[ng-bind^="l.dest"]'
            )

            arrival_city_element = arrival_city_and_code_element[0]

            arrival_city = str(arrival_city_element.get_attribute('innerHTML')).strip()

            arrival_city_code_element = arrival_city_and_code_element[1]

            arrival_city_code = str(arrival_city_code_element.get_attribute('innerHTML')).strip()


            arrival_date_element = single_flight.find_element_by_css_selector(
                'span[ng-bind="l.arrDT"]'
            )
            
            arrival_date = str(arrival_date_element.get_attribute('innerHTML')).strip()

            journey = departure_city + "(" + departure_city_code + ")" " - " + arrival_city + "(" + arrival_city_code + ")"

            flights_details.append([
                flight_number,
                flight_name,
                journey,
                departure_time,
                departure_date,
                arrival_time,
                arrival_date
            ])
        

        table = PrettyTable(
            field_names=["Flight No.", "Flight Name", "Journey", "Dept Time", "Dept Date", "Arr Time", "Arr Date"]
        )

        table.add_rows(flights_details)

        return table
        