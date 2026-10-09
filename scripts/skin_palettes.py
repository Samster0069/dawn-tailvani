"""Per-skin palettes for the rebuild. Roles:
hero  = hero band colour (color_background)     band = secondary band (color_band)
dark  = ink band (color_dark)                    text = text on light bands (color_text)
btn/btn_label = buttons                          A/A2/G/L = prop colours (A = color_accent)
props = prop names used around the arch, in placement-slot order
"""
SKINS = {
 'base':        dict(hero='#F7D9CF', band='#DCE5CF', dark='#2B3524', text='#2B3524', btn='#2B3524', btn_label='#FFFDF8', A='#F2AE3D', A2='#C4673F', G='#7E9A68', L='#FFFDF8',
                     props=['sprig', 'heart', 'dot', 'sprig', 'heart_small', 'ring'], photo='base/base-1', feature='base/base-2'),
 'fall-2026':   dict(hero='#F7CBA6', band='#F3E3BC', dark='#4A2A1C', text='#3A2418', btn='#4A2A1C', btn_label='#FFF8EF', A='#E8833A', A2='#C9502E', G='#8A8B3A', L='#FFF8EF',
                     props=['maple', 'leaf', 'acorn', 'maple', 'leaf', 'acorn'], photo='fall/fall-1', feature='fall/fall-4'),
 'halloween-2026': dict(hero='#F7B46A', band='#E6DCF0', dark='#2A1F33', text='#2A1F33', btn='#2A1F33', btn_label='#FFF8EF', A='#F28C28', A2='#E06A1B', G='#5E7A3A', L='#FFF8EF',
                     props=['pumpkin', 'bat', 'moon', 'bat', 'star_small', 'pumpkin'], photo='halloween/halloween-1', feature='halloween/halloween-3'),
 'national-cat-day-2026': dict(hero='#F1D4DF', band='#F6E7C8', dark='#4B2238', text='#3A1C2C', btn='#4B2238', btn_label='#FFF8F4', A='#E98AA8', A2='#F2AE3D', G='#7E9A68', L='#FFF8F4',
                     props=['yarn', 'paw', 'heart_small', 'paw', 'dot', 'yarn'], photo='catday/catday-3', feature='catday/catday-2'),
 'thanksgiving-2026': dict(hero='#EBC9A0', band='#DDE3C8', dark='#3D2B1F', text='#3D2B1F', btn='#6B3A22', btn_label='#FFF8EF', A='#D98A2B', A2='#B5512C', G='#6F7F3E', L='#FFF8EF',
                     props=['pumpkin', 'maple', 'acorn', 'leaf', 'acorn', 'maple'], photo='thanksgiving/thanksgiving-4', feature='thanksgiving/thanksgiving-3'),
 'bfcm-2026':   dict(hero='#F4C7B1', band='#F9E7C9', dark='#1F3A34', text='#2A2420', btn='#1F3A34', btn_label='#FFF8EF', A='#F2AE3D', A2='#1F3A34', G='#5E8A6E', L='#FFF8EF',
                     props=['gift', 'star', 'sparkle', 'gift', 'star_small', 'sparkle'], photo='bfcm/bfcm-1', feature='bfcm/bfcm-3'),
 'holidays-2026': dict(hero='#F4D3CB', band='#D6E6DA', dark='#1E4636', text='#1E2E26', btn='#1E4636', btn_label='#FFFBF5', A='#E9B44C', A2='#C8323A', G='#2F6B4F', L='#FFFBF5',
                     props=['bauble', 'fir', 'star', 'fir', 'bauble', 'sparkle'], photo='holidays/holidays-2', feature='holidays/holidays-4'),
 'winter-2026': dict(hero='#D7E6F2', band='#EEF0F4', dark='#1F3247', text='#1F3247', btn='#1F3247', btn_label='#FFFFFF', A='#8DB4D6', A2='#FFFFFF', G='#4E7A8A', L='#FFFFFF',
                     props=['snowflake', 'dot', 'snowflake', 'sparkle', 'snowflake', 'dot'], photo='winter/winter-1', feature='winter/winter-2'),
 'new-year-2027': dict(hero='#F1E3C2', band='#E3E6F2', dark='#1E2547', text='#1E2547', btn='#1E2547', btn_label='#FFFDF8', A='#D4A637', A2='#E5566F', G='#1E2547', L='#FFFDF8',
                     props=['burst', 'confetti', 'sparkle', 'confetti', 'star', 'burst'], photo='newyear/newyear-5', feature='newyear/newyear-2'),
 'valentines-2027': dict(hero='#F8C9D0', band='#FBE6E4', dark='#6B1F33', text='#4A1A27', btn='#6B1F33', btn_label='#FFF8F6', A='#F08FA0', A2='#D9364F', G='#7E9A68', L='#FFF8F6',
                     props=['heart', 'heart_small', 'blossom', 'heart', 'dot', 'heart_small'], photo='valentines/valentines-4', feature='valentines/valentines-1'),
 'st-patricks-2027': dict(hero='#F6F0D2', band='#D3EBC8', dark='#1F4A2C', text='#1F3A24', btn='#1F4A2C', btn_label='#FFFDF6', A='#E9B44C', A2='#F2AE3D', G='#3E9150', L='#FFFDF6',
                     props=['shamrock', 'coin', 'shamrock', 'sparkle', 'coin', 'shamrock'], photo='stpatricks/stpatricks-1', feature='stpatricks/stpatricks-3'),
 'tailvani-anniversary-2027': dict(hero='#F9D4E2', band='#FCEBC4', dark='#2B3524', text='#2B3524', btn='#2B3524', btn_label='#FFFDF8', A='#F2AE3D', A2='#E5668A', G='#7E9A68', L='#FFFDF8',
                     props=['balloon', 'party_hat', 'confetti', 'balloon', 'sparkle', 'confetti'], photo='anniversary/anniversary-1', feature='anniversary/anniversary-3'),
 'spring-2027': dict(hero='#F9D3DC', band='#E2EED6', dark='#2F4A2E', text='#2F3A2A', btn='#2F4A2E', btn_label='#FFFDF8', A='#F6C744', A2='#EF8FA8', G='#5E9150', L='#FFFDF8',
                     props=['blossom', 'tulip', 'petal', 'blossom', 'sprig', 'petal'], photo='spring/spring-3', feature='easterb/easter-2'),
 'easter-2027': dict(hero='#E3DDF4', band='#FBF0C9', dark='#3E3A63', text='#2F2B4A', btn='#3E3A63', btn_label='#FFFDF8', A='#A9D8C8', A2='#F2B5CB', G='#6EA383', L='#FFFDF8',
                     props=['egg', 'tulip', 'blossom', 'egg', 'dot', 'petal'], photo='easter/easter-3', feature='easterb/easter-5'),
 'fourth-of-july-2027': dict(hero='#DCE6F4', band='#F6E3DE', dark='#1C2B4D', text='#1C2B4D', btn='#1C2B4D', btn_label='#FFFFFF', A='#C8343B', A2='#2F4F8F', G='#1C2B4D', L='#FFFFFF',
                     props=['star', 'burst', 'bunting', 'star_small', 'burst', 'star'], photo='july4b/july4-1', feature='july4b/july4-3'),
 'summer-2027': dict(hero='#FFE0A3', band='#CFEAF0', dark='#0F4C5C', text='#183A42', btn='#0F4C5C', btn_label='#FFFDF8', A='#F07B4A', A2='#F6C744', G='#3E9A7A', L='#FFFDF8',
                     props=['sun', 'lemon', 'dot', 'lemon', 'sparkle', 'sun'], photo='summer/summer-3', feature='summer/summer-4'),
 'national-dog-day-2027': dict(hero='#FBD7A8', band='#DDE5CF', dark='#2B3524', text='#2B3524', btn='#2B3524', btn_label='#FFFDF8', A='#E07A3F', A2='#C4673F', G='#7E9A68', L='#FFFDF8',
                     props=['bone', 'paw', 'heart_small', 'bone', 'dot', 'paw'], photo='dogdayb/dogday-1', feature='dogdayb/dogday-3'),
}
