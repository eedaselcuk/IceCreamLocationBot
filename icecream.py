
def ask_openai(openai, user_query):
	"""
	Reads the prompt from prompt.txt and sends it to OpenAI, filling in the user_query.
	"""
	try:
		with open("prompt.txt", "r", encoding="utf-8") as f:
			prompt_template = f.read()
		prompt = prompt_template.replace("{user_query}", user_query)
		# openai should be an OpenAI client object
		response = openai.chat.completions.create(
			model="gpt-4o",
			messages=[
				{"role": "system", "content": "You are an assistant."},
				{"role": "user", "content": prompt}
			],
			max_tokens=200,
			temperature=0
		)
		refined = response.choices[0].message.content.strip()
		return refined
	except Exception as e:
		print(f"OpenAI API hatası: {e}")
		return user_query  # fallback
def find_places(gmaps, texts, current_language, query):
	"""
	Searches for cafes, bakeries, ice cream shops, and patisseries on Google Maps, using search_types from localization.py for filtering.
	If no results are found in the current language, tries the alternative language's search_types as fallback.
	"""
	try:
		# Convert city name to coordinates
		geocode = gmaps.geocode(query)
		if not geocode:
			return []

		location = geocode[0]["geometry"]["location"]
		latlng = (location["lat"], location["lng"])

		# Supported types
		allowed_types = ["cafe", "bakery", "restaurant"]

		def get_places(search_types, lang_code):
			found = []
			for place_type in allowed_types:
				results = gmaps.places_nearby(
					location=latlng,
					radius=5000,  # 5 km
					type=place_type,
					language=lang_code
				)
				for place in results.get("results", []):
					name = place.get("name", "").lower()
					if any(word in name for word in search_types):
						address = place.get("vicinity", "")
						rating = place.get("rating", "N/A")
						url = f"https://www.google.com/maps/place/?q=place_id:{place['place_id']}"
						found.append({
							"name": place.get("name", ""),
							"address": address,
							"rating": rating,
							"url": url
						})
			return found

		# Try current language search_types first
		search_types = [s.lower() for s in texts[current_language].get('search_types', [])]
		lang_code = current_language if current_language == 'tr' else 'en'
		places = get_places(search_types, lang_code)

		# If no results, try the other language's search_types as fallback
		if not places:
			alt_lang = 'en' if current_language == 'tr' else 'tr'
			alt_search_types = [s.lower() for s in texts[alt_lang].get('search_types', [])]
			alt_lang_code = alt_lang if alt_lang == 'tr' else 'en'
			places = get_places(alt_search_types, alt_lang_code)

		return places[:3]

	except Exception as e:
		print(f"mistakes by Google Maps API: {e}")
		return []
