# import asyncio
# from playwright.async_api import async_playwright

# async def scrape_himalayas_candidates():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)
#         page = await browser.new_page()
        
#         await page.goto("https://himalayas.app/talent/nodejs", wait_until="domcontentloaded")

#         # Wait for cards to exist in DOM (even if not visible yet)
#         await page.wait_for_selector(".rounded-xl", state="attached")
#         await page.wait_for_timeout(2000)  # wait a bit for JS content

#         candidates = await page.eval_on_selector_all(
#             ".rounded-xl",
#             """cards => cards.map(card => ({
#                 name: card.querySelector("h3 span:first-child")?.innerText.trim() || null,
#                 username: card.querySelector("h3 span.font-normal")?.innerText.trim() || null,
#                 location: card.querySelector("a[href*='/talent/countries'] span")?.innerText.trim() || null,
#                 roles: Array.from(card.querySelectorAll("a[href*='/talent/']:not([href*='/talent/countries']):not([href*='/talent/skills']) span"))
#                            .map(el => el.innerText.trim()),
#                 skills: Array.from(card.querySelectorAll("a[href*='/talent/skills'] span"))
#                             .map(el => el.innerText.trim())
#             }))"""
#         )

#         print(candidates)
#         await browser.close()

# asyncio.run(scrape_himalayas_candidates())

import asyncio
import csv
from playwright.async_api import async_playwright

async def scrape_himalayas_candidates():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://himalayas.app/talent/countries/india/spring-boot", wait_until="domcontentloaded")
        await page.wait_for_selector(".rounded-xl", state="attached")
        await page.wait_for_timeout(2000)  # allow JS content to load

        candidates = await page.eval_on_selector_all(
            ".rounded-xl",
            """cards => cards.map(card => {
                // Basic info
                const name = card.querySelector("h3 span:first-child")?.innerText.trim() || null;
                const location = card.querySelector("a[href*='/talent/countries'] span")?.innerText.trim() || null;

                // Roles
                const roles = Array.from(card.querySelectorAll(
                    "a[href*='/talent/']:not([href*='/talent/countries']):not([href*='/talent/skills']) span"
                )).map(el => el.innerText.trim());

                // Skills
                const skills = Array.from(card.querySelectorAll("a[href*='/talent/skills'] span"))
                                .map(el => el.innerText.trim());

                // Experience
                const experience_cards = Array.from(card.querySelectorAll("div.flex.items-center.gap-x-3"));
                const experience = experience_cards.map(exp => {
                    const position = exp.querySelector("p.font-medium.text-gray-900")?.innerText.trim() || null;
                    const company = exp.querySelector("p.text-sm.font-medium.text-gray-700")?.innerText.trim() || null;
                    return {position, company};
                });

                return {name, location, roles, skills, experience};
            })"""
        )

        await browser.close()
        return candidates

def save_to_csv(candidates, filename="candidates.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["name", "location", "roles", "skills", "experience"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for c in candidates:
            # Flatten roles and skills lists
            c["roles"] = ", ".join(c.get("roles", []))
            c["skills"] = ", ".join(c.get("skills", []))
            # Flatten experience into a string: Position @ Company; ...
            exp_list = c.get("experience", [])
            exp_str = "; ".join([f"{e['position']} @ {e['company']}" for e in exp_list])
            c["experience"] = exp_str
            writer.writerow(c)

async def main():
    candidates = await scrape_himalayas_candidates()
    save_to_csv(candidates)
    print(f"Saved {len(candidates)} candidates to CSV!")

asyncio.run(main())
