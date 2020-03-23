import requests


class ImageManager:
    images_folder = 'C:\\Users\\facel\\sneaker_images\\'
    image_extension = '.jpg'

    def download_images(self, items_dict):
        for key, value in items_dict.items():
            article, image_url = key.replace('\r', ''), value[0].image_url
            img_data = requests.get(image_url).content

            print(article)

            try:
                with open('{}{}{}'.format(self.images_folder, article, self.image_extension), 'wb') as handler:
                    handler.write(img_data)

            except Exception as e:
                print(e)
                # article = 'failed-image-' + str(failed_image_load_index)
                # failed_image_load_index += 1