
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
def find_places(gmaps, query):
	"""
	Searches for cafes, bakeries, ice cream shops, and patisseries on Google Maps near the given query location.
	"""
	try:
		geocode = gmaps.geocode(query)
		if not geocode:
			return []

		location = geocode[0]["geometry"]["location"]
		latlng = (location["lat"], location["lng"])
		allowed_types = ["cafe", "bakery", "restaurant"]
		found = []
		for place_type in allowed_types:
			results = gmaps.places_nearby(
				location=latlng,
				radius=5000,
				type=place_type,
				language='en'
			)
			for place in results.get("results", []):
				address = place.get("vicinity", "")
				rating = place.get("rating", "N/A")
				url = f"https://www.google.com/maps/place/?q=place_id:{place['place_id']}"
				found.append({
					"name": place.get("name", ""),
					"address": address,
					"rating": rating,
					"url": url
				})
		return found[:3]
	except Exception as e:
		print(f"mistakes by Google Maps API: {e}")
		return []
