---
name: Lidija Torte i Kolači
description: A cake box from a family workshop in Leskovac, opened on arrival.
colors:
  satin-pink: "#F7ACBC"
  berry-shade: "#DB6E9D"
  berry: "#A23D6B"
  sprinkle-gold: "#FDB933"
  sprinkle-sky: "#00ABE6"
  viber: "#7360F2"
  whatsapp: "#1FAF5A"
  plum-ink: "#3B2430"
  plum-soft: "#6B4757"
  praline-plum: "#4A2E3B"
  blush: "#FDE9EE"
  mist: "#FFF6F8"
  box-board: "#FFFFFF"
  slip-paper: "#FFFDF9"
  hairline: "#F6D3DC"
  perforation: "#EFC6D1"
  on-plum: "#F6E6EC"
  on-plum-soft: "#E9CDD7"
typography:
  display:
    fontFamily: "Shrikhand, Georgia, serif"
    fontSize: "clamp(2.7rem, 5.6vw, 5rem)"
    fontWeight: 400
    lineHeight: 1.08
    letterSpacing: "-0.01em"
  headline:
    fontFamily: "Shrikhand, Georgia, serif"
    fontSize: "clamp(2.2rem, 4.6vw, 3.8rem)"
    fontWeight: 400
    lineHeight: 1.08
    letterSpacing: "-0.01em"
  title:
    fontFamily: "Shrikhand, Georgia, serif"
    fontSize: "clamp(1.5rem, 2.2vw, 1.9rem)"
    fontWeight: 400
    lineHeight: 1.1
  title-plain:
    fontFamily: "Figtree, system-ui, sans-serif"
    fontSize: "1.35rem"
    fontWeight: 700
    lineHeight: 1.2
  body:
    fontFamily: "Figtree, system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.6
  lead:
    fontFamily: "Figtree, system-ui, sans-serif"
    fontSize: "clamp(1.08rem, 1.4vw, 1.22rem)"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Barlow Condensed, Arial Narrow, sans-serif"
    fontSize: "0.85rem"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0.18em"
  label-nav:
    fontFamily: "Barlow Condensed, Arial Narrow, sans-serif"
    fontSize: "1rem"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "0.06em"
  hand:
    fontFamily: "Caveat, cursive"
    fontSize: "1.45rem"
    fontWeight: 700
    lineHeight: 1.15
rounded:
  print: "4px"
  board: "10px"
  well: "14px"
  tray: "16px"
  window: "18px"
  praline-box: "22px"
  pill: "999px"
  seal: "50%"
spacing:
  gutter: "clamp(16px, 4vw, 56px)"
  container: "1240px"
  section: "clamp(80px, 10vw, 130px)"
  stack-sm: "12px"
  stack-md: "22px"
  stack-lg: "30px"
components:
  button-viber:
    backgroundColor: "{colors.viber}"
    textColor: "{colors.box-board}"
    rounded: "{rounded.pill}"
    padding: "0 1.3em"
    height: "52px"
  button-viber-hover:
    backgroundColor: "#6150E0"
  button-whatsapp:
    backgroundColor: "{colors.whatsapp}"
    textColor: "{colors.box-board}"
    rounded: "{rounded.pill}"
    padding: "0 1.3em"
    height: "52px"
  button-whatsapp-hover:
    backgroundColor: "#189A4E"
  button-ink:
    backgroundColor: "{colors.plum-ink}"
    textColor: "{colors.box-board}"
    rounded: "{rounded.pill}"
    padding: "0 1.3em"
    height: "52px"
  button-line:
    backgroundColor: "transparent"
    textColor: "{colors.plum-ink}"
    rounded: "{rounded.pill}"
    padding: "0 1.3em"
    height: "52px"
  button-line-hover:
    backgroundColor: "{colors.box-board}"
  button-small:
    rounded: "{rounded.pill}"
    padding: "0 1em"
    height: "42px"
  nav-link:
    textColor: "{colors.plum-soft}"
    typography: "{typography.label-nav}"
    padding: "8px 0"
  nav-link-hover:
    textColor: "{colors.plum-ink}"
  print:
    backgroundColor: "{colors.box-board}"
    rounded: "{rounded.print}"
    padding: "12px 12px 18px"
  order-slip:
    backgroundColor: "{colors.slip-paper}"
    textColor: "{colors.plum-ink}"
    typography: "{typography.hand}"
    padding: "22px 18px 16px"
  praline-well:
    backgroundColor: "#352029"
    textColor: "{colors.on-plum}"
    rounded: "{rounded.well}"
    padding: "16px 8px 14px"
  sticker:
    backgroundColor: "{colors.sprinkle-gold}"
    textColor: "{colors.plum-ink}"
    rounded: "{rounded.seal}"
    size: "168px"
  gift-tag:
    backgroundColor: "{colors.box-board}"
    textColor: "{colors.plum-ink}"
    padding: "34px 36px 32px 64px"
  phone-dock:
    backgroundColor: "rgb(255 255 255 / .94)"
    rounded: "20px"
    padding: "6px"
---

# Design System: Lidija Torte i Kolači

## Overview

**Creative North Star: "The Ribboned Cake Box"**

The whole site is a white cake box from Lidija's workshop, set on a blush counter. On arrival the satin bow unties, the ribbon slides off, and the box stands open with its lid leaning behind it, a loosened bow on the lid corner and the ribbon draped over the front edge. Everything after that is the paperwork and packaging of a real cake order: taped photo prints, a handwritten order slip, a praline box of flavours, a receipt with a perforated edge, an airmail postcard, a gift tag on a satin cord.

The mood is joyful, warm and handmade, with a confident display face that sounds like a celebration and a body face that stays plain and readable for older relatives on phones. Depth comes from paper and board lying on a surface: soft plum-tinted shadows pooled under each object and small rotations, so nothing sits perfectly square. Colour is mostly pink and white, as the logo demands, with plum ink for every word and the logo's blue and gold scattered as sprinkles, tape and stickers. The descriptive language here was derived from the direction contract and the shipped build, without a user interview.

The direction contract planned a wrapped box that unties on load. The build, approved in review, ends on the opened box; that end state is the canonical hero and is also what reduced-motion and no-JS visitors see.

**Key Characteristics:**
- White box board on a blush counter, with a dark chocolate-plum band for the flavour box and the contact footer.
- Every object is a physical thing from a cake order: print, slip, receipt, tag, sticker, seal, doily, washi tape.
- Four typefaces, each with one job: Shrikhand celebrates, Figtree explains, Barlow Condensed prints labels, Caveat writes by hand.
- Plum-tinted soft shadows and small tilts carry all depth.
- Motion is physical and answers the visitor: the ribbon unties once, sprinkles burst on press, the occasions band moves with scroll.
- Viber and WhatsApp buttons are always within reach; on phones a docked bar holds them.

## Colors

A sugared palette of satin pink and white board, written in plum ink, with the logo's gold and sky blue scattered as sprinkles.

### Primary
- **Satin Pink** (satin-pink): the ribbon itself. Used for the occasions band, nav underline, step-number discs, the pink round sticker, Instagram "more" tile, text selection and headlines on the plum ground.
- **Berry Shade** (berry-shade): the shaded fold of the satin. Focus outlines, the filled part of the guest slider, checkbox outlines on the order slip, the scrollbar thumb and the doily airmail stripe.

### Secondary
- **Berry** (berry): the deepest pink, used as a text colour on white and blush. Brand name in the header, print captions, handwritten emphasis, box labels printed on paper, the large guest count and price emphasis.

### Tertiary
- **Sprinkle Gold** (sprinkle-gold): rating stars, the gold sticker and stat seal, washi tape, foil lines around the praline box and tray labels on plum.
- **Sprinkle Sky** (sprinkle-sky): washi tape on the hero slip, airmail stripes on the postcard, and sprinkles.
- **Viber Purple** (viber) and **WhatsApp Green** (whatsapp): platform action colours for the buttons that open those apps. WhatsApp green also inks the tick marks on the order slip and receipt.

### Neutral
- **Plum Ink** (plum-ink): every headline and body word on light ground, the default button fill, and the chocolate surface of the flavour section and footer. It is defined twice in CSS (`--ink` and `--choc`) with the same value.
- **Soft Plum** (plum-soft): secondary copy, leads, nav links, notes.
- **Praline Plum** (praline-plum): the praline box sitting on the chocolate section.
- **Blush** (blush): the page counter every box and print sits on.
- **Mist** (mist): the receipt paper.
- **Box Board** (box-board): the box, prints, postcard, header glass, gift tag and order section.
- **Slip Paper** (slip-paper): the warm-white handwriting paper of order slips, ruled with hairline pink lines.
- **Hairline** (hairline): header bottom border, unfilled slider track, slip ruling.
- **Perforation** (perforation): dashed tear lines on the receipt, postcard divider and handwriting lines.
- **On Plum** (on-plum) and **On Plum Soft** (on-plum-soft): body text and secondary text on the chocolate surface.

### Named Rules
**The Plum Ink Rule.** Every word is plum ink, soft plum or berry on light ground, and on-plum or satin pink on the chocolate ground. Pure black text never appears.

**The Sprinkle Rule.** Gold and sky blue appear only as sprinkles, stars, tape, stickers, stamps and thin foil lines. They never fill a section and never set body text.

**The Messenger Rule.** Viber purple and WhatsApp green belong to the buttons that open those apps (plus the green tick of a completed item). No other control borrows them.

## Typography

**Display Font:** Shrikhand (with Georgia, serif)
**Body Font:** Figtree (with system-ui, sans-serif)
**Label Font:** Barlow Condensed (with Arial Narrow, sans-serif)
**Hand Font:** Caveat (with cursive)

**Character:** A plump, celebratory script-like display paired with a friendly geometric sans, plus a condensed printer's label face for things stamped on packaging and a handwriting face for things written on paper.

### Hierarchy
- **Display** (Shrikhand 400, clamp(2.7rem, 5.6vw, 5rem), line-height 1.08): the hero headline only. Drops to clamp(2.5rem, 10vw, 3.6rem) below 900px.
- **Headline** (Shrikhand 400, clamp(2.2rem, 4.6vw, 3.8rem), 1.08): section headings, centred over the section or set left beside content. Satin pink on the chocolate ground.
- **Title** (Shrikhand 400, clamp(1.5rem, 2.2vw, 1.9rem), 1.1): captions on photo prints, in berry. Shrikhand also sets big numerals (guest count, phone numbers, sticker figures, step numbers).
- **Title Plain** (Figtree 700, 1.35rem, 1.2): step titles in the ordering sequence, where several titles stack.
- **Body** (Figtree 400, 1.0625rem, 1.6; 1rem on phones): running copy, held to 44 to 58ch.
- **Lead** (Figtree 400, clamp(1.08rem, 1.4vw, 1.22rem)): the hero lead and section intros, max 34ch in the hero.
- **Label** (Barlow Condensed 700, 0.85rem to 1.1rem, letter-spacing 0.1em to 0.32em, uppercase): text printed on packaging: the order slip header, praline tray names, the vertical print on the box side, stamp captions, receipt footer.
- **Label Nav** (Barlow Condensed 600, 1rem, 0.06em, uppercase): header navigation and the occasions band (700, clamp(1.3rem, 2.4vw, 1.9rem)).
- **Hand** (Caveat 500 to 700, 1.28rem to 1.85rem): handwriting on slips, receipt checklist, cake tag, postcard lines and short notes.

### Named Rules
**The Four Hands Rule.** Each face has one job. Shrikhand celebrates (headings, big numbers, the brand name), Figtree explains, Barlow Condensed is printed on packaging, Caveat is written by a person on paper. A face never takes another face's job.

**The Short Hand Rule.** Caveat sets one line or a short list item at a time. Paragraphs are always Figtree.

## Layout

Content sits in a centred container of 1240px with a fluid side gutter of clamp(16px, 4vw, 56px). Sections breathe with vertical padding of clamp(80px, 10vw, 130px), rising to a 140px cap on the occasions and about sections, alternating ground: blush counter, a tilted satin band, blush collage, chocolate flavour box, blush calculator, white order section, blush about and Instagram, a postcard, and a chocolate footer that drips into the page with a scalloped edge.

The hero is a two-column grid (0.92fr text, 1.08fr box stage). The occasions collage uses a 12-column grid where prints span different widths (7, 5, 4 columns) and rows, with small rotations, so no two items match. The praline box uses a 2fr / 4fr / 2fr tray grid. Calculator, order, about and contact use two equal or 0.8 / 1.2 columns.

Responsive behaviour: at 1080px the header nav hides. At 900px every grid collapses to one column, the box stage moves above the headline, the collage becomes two columns, and the calculator reorders so the slip, cake drawing and WhatsApp button stack. At 640px the collage is one column, the header Viber button hides, hero buttons stretch, and a fixed three-button phone dock (Viber, WhatsApp, call) slides up once the hero buttons scroll away. The page never scrolls sideways (`overflow-x: clip` on html and body).

## Elevation & Depth

Depth is paper and board lying on a counter. Each object casts a soft shadow tinted plum, offset downward with a negative spread so it pools under the object; light-ground shadows use rgb(116 46 78) or rgb(59 36 48), and only the chocolate section uses black. Board edges get a 1px to 2px hairline lip in pink grey to read as thickness. Satin elements (bow, loose ribbon, tag cord) use filter drop-shadows so the shadow follows their shape. Tilt is the second depth cue: sheets sit between -5deg and +2deg, stickers, seals and postmarks up to 14deg.

### Shadow Vocabulary
- **Button lift** (`box-shadow: 0 6px 14px -6px rgb(59 36 48 / .45)`, hover `0 10px 20px -8px rgb(59 36 48 / .5)` with a 2px rise): filled pill buttons.
- **Print** (`box-shadow: 0 1px 0 #F1D3DB, 0 22px 30px -22px rgb(116 46 78 / .5)`): photo prints and the about photo.
- **Box** (`box-shadow: 0 2px 0 #F3D7DE, 0 30px 50px -28px rgb(116 46 78 / .45), 0 12px 24px -16px rgb(116 46 78 / .3)`): the cake box, with skewed side and bottom faces in pink-grey gradients.
- **Paper slip** (`box-shadow: 0 14px 22px -14px rgb(59 36 48 / .5)`): order slips and the calculator slip.
- **Sticker** (`box-shadow: 0 12px 20px -12px rgb(116 46 78 / .5)`): stickers and round stat seals.
- **Satin** (`filter: drop-shadow(0 6px 6px rgb(116 46 78 / .28))`): bow, loose ribbon, lid bow.
- **Praline well** (`box-shadow: inset 0 2px 6px rgb(0 0 0 / .45)`): recessed compartments on the chocolate ground.

### Named Rules
**The Plum Shadow Rule.** On light ground every shadow is plum-tinted with negative spread. Grey or black shadows on blush or white never appear.

**The Tilted Paper Rule.** Paper objects tilt slightly; stickers and seals tilt more. Buttons, navigation, body copy and form controls stay level.

## Shapes

Buttons and the slider are full pills (999px). The box board has gently rounded corners (10px) and its die-cut window is softer (18px) with a white inner frame. Photo prints are crisp (4px) with a white border thicker at the bottom, like an instant print. The praline box (22px), trays (16px) and wells (14px) step down in radius as they nest. Stickers, seals, stat discs, step numbers and bonbons are circles.

Recurring silhouettes, each built in CSS or SVG: washi tape with zig-zag torn ends (conic-gradient mask), a receipt with a scalloped bottom edge (radial mask), a gift tag with a clipped arrow end and a punched eyelet, a cake tag in the same shape, a paper lace doily (`assets/doily.svg`), an airmail border of berry and sky stripes, a stamp with a dotted inner outline, a round postmark, and a scalloped chocolate drip at the top of the footer. Ruled paper uses repeating pink hairlines.

## Components

### Buttons
Round, plump and tactile, like a candy.
- **Shape:** full pill (999px), 52px tall (42px small), icon plus label, Figtree 600 at 1.02rem.
- **Primary:** Viber purple for "send a photo on Viber", WhatsApp green beside it. The plain filled variant is plum ink.
- **Hover / Focus:** rises 2px with a deeper shadow over 0.25s on the house ease; Viber and WhatsApp darken slightly. Focus is a 3px berry-shade outline at 3px offset. Pressing a contact button bursts a small handful of sprinkles from the pointer.
- **Line:** transparent with a 2px plum ink border and no shadow; fills with white on hover.
- **Call link:** a phone line under the buttons, number bold with a satin-pink underline that deepens on hover.

### Navigation
Sticky header on white glass (92% white, 10px blur, saturated) with a hairline pink bottom border. Logo plus the brand name in berry Shrikhand with a tracked Barlow subline. Links are uppercase Barlow Condensed in soft plum; on hover the text turns plum ink and a 3px satin-pink bar grows from the left. A small Viber pill closes the bar. On phones the links and pill hide and the fixed phone dock takes over: three rounded tiles (Viber, WhatsApp, call in plum) on a white glass tray.

### Cards / Containers
Containers are always a physical object from the order.
- **Print:** white board, 4px corners, 12px padding with 18px at the bottom, print shadow, small tilt, one or two pieces of washi tape across the top edge, Shrikhand caption in berry.
- **Order slip:** slip paper ruled with hairline pink, Caveat text, a Barlow label header in berry, a strip of tape at the top, tilted -1deg to -5deg.
- **Receipt:** mist paper with a scalloped bottom, a Shrikhand title in berry, a handwritten checklist with berry-shade boxes and green ticks, a dashed perforation above the footer.
- **Postcard:** white card with an airmail-stripe border, dashed divider, stamp and round postmark, handwritten address lines.
- **Gift tag:** white tag with an arrow-clipped left end and an eyelet, hung on a satin cord, carrying the phone numbers in Shrikhand.

### Inputs / Fields
The only input is the guest-count slider: a 12px pill track (berry-shade fill, hairline remainder) with a 34px white thumb ringed 4px in berry-shade. The count above it is a large berry Shrikhand numeral.

### Cake Box (signature)
The hero stage. A white board box with a fine paper-noise texture, skewed side and bottom faces, and a square die-cut window showing a real cake photo. Behind it a lid leans at -9deg with the logo script; a loosened bow rests on the lid corner, a satin ribbon drapes over the front edge, a doily and logo seal sit at the lower left corner, the handwritten order slip is taped at the upper left, and a few sprinkles lie on the counter. On load (motion allowed): the bow loops and tails fall away, the horizontal ribbon slides out left and the vertical one drops, a shine crosses the window film, sprinkles pop out of the box, then the seal, slip, loose ribbon, lid bow and landed sprinkles settle in sequence over about 2.8s. Tapping the cake gives another shower.

### Praline Box (signature)
The flavour menu on the chocolate ground: a praline-plum box with a gold foil inset line, trays with double gold hairlines, and recessed wells each holding a coloured bonbon (with a ruffled paper cup made from a repeating conic gradient). Favourites get a gold cup, a satin-pink inner ring and a handwritten heart note. Wells lift 3px on hover and the bonbon tips.

### Growing Cake (signature)
The calculator drawing: an SVG cake whose tiers drop in from above (0.6s, house ease) as the guest count rises from one to four tiers, with the candle riding to the top tier, and a white cake tag naming the size in Caveat.

### Occasions Band
A satin ribbon strip tilted -1.6deg, full bleed, listing occasions in uppercase Barlow Condensed separated by sprinkle bars. It moves sideways with page scroll and stays still otherwise.

## Do's and Don'ts

### Do:
- **Do** make every new container an object from a cake order (print, slip, receipt, tag, sticker, postcard) with a plum-tinted pooled shadow and a small tilt.
- **Do** keep a Viber and a WhatsApp button in every section that ends in an action, Viber first, and keep the phone number one tap away.
- **Do** use real cake photographs from the workshop, framed as prints or inside the box window.
- **Do** run motion on the house ease (`cubic-bezier(.16, 1, .3, 1)`) and make the final, opened state the default markup, so reduced-motion and no-JS visitors see the opened box.
- **Do** set headlines in Shrikhand at weight 400 in plum ink, and keep running copy in Figtree at 44 to 58ch.
- **Do** keep gold and sky blue at sprinkle scale: tape, stickers, stars, foil lines.

### Don't:
- **Don't** set the page as a cream ground with a serif headline over a stock hero and a row of three equal cards; occasions are taped prints of different sizes and tilts.
- **Don't** use pure black text or grey shadows on light ground.
- **Don't** use stock photography or illustrated cakes in place of the workshop's own photos.
- **Don't** run motion that loops on its own; the intro plays once, the band follows scroll, sprinkles answer a press.
- **Don't** rotate buttons, navigation, form controls or paragraphs.
- **Don't** set paragraphs in Caveat or Barlow Condensed.
