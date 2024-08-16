# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        ## Strip the white spaces from strings
        field_names = adapter.field_names() 
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()


        ## Category & Product type -> switch to lower case
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()


        ## Price convert to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value[1:]
            adapter[price_key] = float(value)


        ## Availability -> extract number of books in stock
        availablity_string = adapter.get('avail')
        split_string_array = availablity_string.split('(')

        if len(availablity_string) < 2:
            adapter['avail'] = 0
        else:
            availablity_array = split_string_array[1].split(' ')
            adapter['avail'] = int(availablity_array[0])
        

        ## Reviews -> string to number
        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)


        ## Stars -> convert text to number
        stars_string = adapter.get('stars')
        split_stars_array = stars_string.split(' ')
        stars_text_value = split_stars_array[1].lower()

        if stars_text_value == "zero":
            adapter['stars'] = 0
        elif stars_text_value == "one":
            adapter['stars'] = 1
        elif stars_text_value == "two":
            adapter['stars'] = 2
        elif stars_text_value == "three":
            adapter['stars'] = 3
        elif stars_text_value == "four":
            adapter['stars'] = 4
        elif stars_text_value == "five":
            adapter['stars'] = 5

        '''
        ratings = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
        rating = adapter.get("stars")
        if rating:
            adapter["stars"] = ratings[rating]
        '''
        return item
