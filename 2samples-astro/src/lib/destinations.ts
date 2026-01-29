export interface VideoSection {
  title: string;
  videoName: string;
  description: string;
}

export interface Destination {
  id: string;
  title: string;
  pageTitle: string;
  sections: VideoSection[];
}

export const destinations: Record<string, Destination> = {
  japan: {
    id: 'japan',
    title: 'JAPAN 2019',
    pageTitle: 'JAPAN',
    sections: [
      {
        title: 'Day One - Day Three Osaka',
        videoName: 'Japan-2019-Osaka',
        description: '<strong>Osaka:</strong> We landed late in the evening after a 15+ hour flight.',
      },
      {
        title: 'Day Four Nagoya',
        videoName: 'Japan-2019',
        description: '<strong>Nagoya:</strong> Rode the Bullet Train from Osaka, made the mistake of leaving at rush-hour, the trains to get to the Bullet were packed!',
      },
      {
        title: 'Day Five - Seven Tokyo',
        videoName: 'Tokyo',
        description: '<strong>Tokyo:</strong> Our final city on the trip Tokyo! Amazing city ahead of the 2020 Olympics that got pushed due to Covid. Enjoyed our time, not sure I want to go back.',
      },
    ],
  },
  ireland: {
    id: 'ireland',
    title: 'REPUBLIC OF IRELAND',
    pageTitle: 'REPUBLIC OF IRELAND',
    sections: [
      {
        title: 'Day One',
        videoName: 'Ireland-Scotland-Day-One',
        description: '<strong>Day One:</strong> 26-27 May 2023 - Orlando to Dublin. We left Orlando at 20:30 on Friday and arrived in Dublin at 10:00 on Saturday.',
      },
      {
        title: 'Day Two',
        videoName: 'Ireland-Scotland-Day-Two',
        description: '<strong>Day Two:</strong> 28 May 2023 - Our day started with an Irish Breakfast and a surprise car show. We visited the Guinness tour and Trinity College.',
      },
      {
        title: 'Day Three',
        videoName: 'Ireland-Scotland-Day-Three',
        description: '<strong>Day Three:</strong> 29 May 2023 - Testing Jay\'s ability to drive on the "wrong" side of the road. We made it to Blarney Castle and the English Market in Cork.',
      },
      {
        title: 'Day Four',
        videoName: 'Ireland-Scotland-Day-Four',
        description: '<strong>Day Four:</strong> 30 May 2023 - Farm Day! We visited the Cliffs of Moher and Kylemore Farms for cheese making.',
      },
    ],
  },
  uk: {
    id: 'uk',
    title: 'UNITED KINGDOM',
    pageTitle: 'UNITED KINGDOM',
    sections: [
      {
        title: 'Day Five',
        videoName: 'Ireland-Scotland-Day-Five',
        description:
          '<strong>Day Five:</strong> 31 May 2023 - We left Galway, Ireland and headed north into the United Kingdom, first stopping in the beautiful villeage of Donegal to have lunch at a gastropub that was not open...whoops! The great thing about Ireland is if the place you want to go is no longer there, there is bound to be a pub with some good food nearby. From there we went to the Giants Causeway, this is an abosolute must stop if you are ever visiting anywhere on the Emerald Isle! One of the most amazing places I have ever visited, a place where the words of the Apostle Paul com to life and God\'s invisible attributes become visible. We then made our way to Derry for the night, unfortunately we were all a little road weary and did not do teh Derry Girls tour, check out the Netflix series if you haven\'t. Provides comedy and a history of Northern Ireland\'s "troubles" period.',
      },
      {
        title: 'Day Six',
        videoName: 'Ireland-Scotland-Day-Six',
        description:
          '<strong>Day Six:</strong> 1 June 2023 - We started the day with a Tesco breakfast, after eating out so much a trip to the grocery store was just what was needed. We then made the short drive to Belfast arriving just in time for our reservations at the Yellow Onion and Yardbird. After a delisious lunch the girls went shopping while the boys went to the pubs. The first pub had Poitin on offer, this is the Irish version of moonshine (uncasked whiskey) that we had heard about in the stories at the Hooley in Dublin. It\'s pretty much the same as American moonshine and would serve better as paint remover. Belfast is a beautiful city and we look forward to returning to explore more. We capped the evening off with an outstanding seafood dinner at Mourne Seafood, another must-stop destination!',
      },
      {
        title: 'Day Seven',
        videoName: 'Ireland-Scotland-Day-Seven',
        description:
          '<strong>Day Seven:</strong> 2 June 2023 - Day seven featured a return to Dublin to catch a flight to Glasgow, Scotland. After dropping the girls and the travel bags at the airport, Jay and Tray drove back to the city to pick up the bags that the hotel had stored. See day one and how an Irish rental car is not made for six people and luggage. We rode Ryan Air and got to experience what air travel was like in the days before the terminal bridges, boarding from an outdoor ladder. The flight provided much beautiful scenery and we were able to find a taxi that fit six people and all the bags. We had dinner in Glasgow and got to experience some of the local color…a drunk singing at the top of his lungs.',
      },
      {
        title: 'Day Eight',
        videoName: 'Ireland-Scotland-Day-Eight',
        description:
          '<strong>Day Eight:</strong> 3 June 2023 - We started in Glasgow by picking up the rental car which surprisingly fit not only six people but the original and additional bags that had been picked up along the way. Good thing too, we were setting out on a long journey to see Loch Ness and if we could catch a glimpse of Nessie. The first stop of the day was to Semple Castle, Loch, and grounds for a glimpse of the history of the Samples name. Through research on ancestry.com Jay has determined that he is the 10th great grandson of the 5th Lord of Semple, Hugh Semple. Unfortunately, we did not have time to take the one-mile walk (yes, in the UK they have not converted to metric yet either) to the castle. Instead, we visited with the staff at the visitor\'s center about the relation to the Semples, they produced a flag and guest book for us to pose with and sign. Was a beautiful place and it is located on the approach path from the West if you ever fly into Glasgow airport. Next, we headed north. With it being a Saturday, and an unusually beautiful one at that, it seemed like most of the Glasgow population was also headed north. Their destination was Loch Lomond for a day at the beach, so once we got past that, the unusual amount of traffic cleared up. Driving over there was different, and Scotland was no exception, nothing like passing a tour bus within inches and also having a rock wall on your left! We had lunch at an awesome pub in Fort William and made it to Inverness driving by Loch Ness. No sightings of the beast but was a beautiful drive.',
      },
      {
        title: 'Day Nine',
        videoName: 'Ireland-Scotland-England-Day-Nine',
        description:
          '<strong>Day Nine:</strong> 4 June 2023 - We set out to find Sydney\'s families castle at Caerlaverock in southern Scotland. This castle belonged to the Maxwell clan and was in pretty good shape for being almost 1000 years old. Sydney did not pass up the opportunity to point out which family had the biggest castle, the woman at the Semple Loch visitor center warned us about feuding clans \u{1F642} Since we were just a few miles from the English Border, the reason Caerlaverock was the sight of an English siege in 1300, we decided to have lunch in Carlisle. Looking at Google Maps, Wales was only a 2.5 hour drive from Carlisle, but since we had covered so many miles and kilometers already, decided it would wait for the next trip. From Carlise we went to stay in a real castle! The Melville Castle Hotel is located right outside of Edinburgh and was possibly the highlight of the whole trip. We had dinner delivered to the room, which had a dining room! Explored the grounds and generally relaxed from a long vacation. Was the perfect respite after much travelling.',
      },
      {
        title: 'Day Ten',
        videoName: 'Edinburgh-Day-Ten',
        description:
          '<strong>Day Ten:</strong> 5 June 2023 - The last day of the trip was spent in Edinburgh, its pronounced Eddin-burrah not Edenburg. Trust me you\'ll want to practice unless you want English lessons from everyone in Scotland. We started off with the Johhnie Walker tour, if you are studying Marketing this should count for at least a three-hour class, was very impressive. Once that was done, we had reservations for their rooftop restaurant which provided sweeping views of the entire city. We then headed to the National Museum because they had just put the Declaration of Arbroath on display for the first time in eighteen years. This document was a declaration of independence from the English written in 1320, a 450-year predecessor to the US DOI, signed by the Maxwell Clan via a wax seal, some of which were still intact, but unsure whether the Maxwell one was or not. On the recommendation of a work colleague, we had booked the underground Edinburgh tour, we met the tour guide and explored the system of underground spaces that resulted from the expansion of the city needing to go vertical due to lack of space within the city walls. It provided an excellent history lesson and an insight into the sometimes wretched living conditions of the past. We completed the night with a dinner at Makar\'s Mash a mashed potato restaurant, highly recommended.',
      },
      {
        title: 'Day Eleven',
        videoName: 'Edinburgh-Day-Eleven',
        description:
          '<strong>Day Eleven:</strong> 6 June 2023 - "Leaving on a jet plane, don\'t know when I\'ll be back again…" Our trip complete we caught a cab to the Edinburgh airport to head back to Dublin and then Orlando. The trip was amazing, let us know if you need any tips on where to go and what to do. Overall, we saw as much as we could, looking forward to going back someday and spending more time at the highlights.',
      },
    ],
  },
  greece: {
    id: 'greece',
    title: 'GREECE 2025',
    pageTitle: 'GREECE',
    sections: [
      {
        title: 'Day One',
        videoName: 'Greece-Day-1',
        description:
          '<strong>Day One:</strong> May 9-10, 2025 Miami to Athens: After a ten and a half-hour flight we arrived in Athens. Once we received out bags and cleared customs we got into a taxi driven by Nikkos who expertly drove us into the city center. This trip was quite an experience around the tiny streets, lined on both sides with parked cars. Let\'s just say that we are going to be extra careful walking about the city because over here pedestrians don\'t seem to have the right-of-way. We arrived at our hotel around noon, an amazing spot with a sidewalk cafe on a sycamore lined street. After checking in and a quick nap we headed out to explore. The weather was perfect and we walked around the Acropolis taking in the many sidewalk performers that were out Saturday afternoon. We found a rooftop cafe and sampled some greek cuisine. I was not 100% but the grilled octopus they served quickly revived me. Once we had eaten we headed out to shop, there were many shops close by and we enjoyed seeing all that they had to offer. We closed the night out with dinner at the Sense restaurant at the top of the hotel. The menu was a chef\'s tasting and was an amazing offering of local flavors and presentations. We dined and watched the sunset on the Parthenon.',
      },
      {
        title: 'Day Two',
        videoName: 'Greece Day 2',
        description:
          '<strong>Day Two:</strong> May 11, 2025 Athens and Boarding the Resilient Lady Virgin Cruise Ship. Outstanding weather, we could see our ship in the harbor from the top of the Parthenon!',
      },
      {
        title: 'Days Three and Four',
        videoName: 'Greece Day 3&4',
        description:
          '<strong>Day Three:</strong> May 12-13, 2025 Sea Day and Rhodes Wine Tour: Had an awesome time in Rhodes seeing all the history and tasting awesome wines and olive oils!',
      },
      {
        title: 'Day Five',
        videoName: 'Greece Day 5',
        description:
          '<strong>Day Four:</strong> May 14, 2025 Bodrum Turkey, Ephesus, and Virgin Mary House. This was a long day, 2.5 hour drive each direction, but overall was amazing to see the beautiful country of Turkey!',
      },
      {
        title: 'Day Six',
        videoName: 'Greece Day 6',
        description:
          '<strong>Day Four:</strong> May 15, 2025 Santorini Catamaran Sailing. Swam in a volcano, air temp was 64, water temp 65, so water was warm! :)',
      },
      {
        title: 'Days Seven and Eight',
        videoName: 'Greece Days 7&8',
        description:
          '<strong>Day Four:</strong> May 16-17, 2025 Chania, Crete. We were supposed to go to Mykonos but the weather was bad. Did some shopping and exploring the town. When we pulled into port the sky was full of dust.',
      },
    ],
  },
  bahamas: {
    id: 'bahamas',
    title: 'BAHAMAS 2025',
    pageTitle: 'BAHAMAS',
    sections: [
      {
        title: 'Fourth of July Cruise',
        videoName: 'Bahamas 2025',
        description: '<strong>Bahamas:</strong> Fourth of July cruise with Sydney\'s parents! Cape Canaveral to Nassau and MSC\'s private cay.',
      },
    ],
  },
};
