from creator import Creator


class CreatorExtractor:

    def __init__(self, page):
        self.page = page

    def extract_visible_creators(self):

        creators = []

        #invite_buttons = self.page.get_by_role("button", name="Invite")

        #count = invite_buttons.count()

        #print(f"Found {count} visible creators")
        rows = self.page.locator("tbody tr")

        count = rows.count()

        print(f"Found {count} creator rows")

        
        for i in range(count):
            row = rows.nth(i)

            creator = self.extract_creator(row)

            creators.append(creator)
        return creators

    def extract_creator(self, row):

        creator = Creator()

        # We'll fill this method next

        return creator