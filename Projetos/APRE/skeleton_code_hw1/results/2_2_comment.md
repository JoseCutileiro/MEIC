# ============== 2 . 2 . a =================

Como é obvio o b1024 é muito mais rápido a executar que o b16, \
mas não há almoços grátis perdendo valor nos resultado atingidos. \
Ainda assim pode ser util em alguns use cases.

## b16
1. Valid acc: 0.8193
2. Final test acc: 0.7713
3. Time: 136.40 seconds
 
## b1024

1. Valid acc: 0.6956
2. Final test acc: 0.7278
3. Time: 31.78 seconds

# ============== 2 . 2 . b =================

## lr 1 

1. Valid acc: 0.4721
2. Final test acc: 0.4726
3. Time:

## lr 0.1 

1. Valid acc: 0.8193
2. Final test acc: 0.7713
3. Time: 129.28

## lr 0.01

1. Valid acc: 0.8175
2. Final test acc: 0.7505
3. Time: 135.65

## lr 0.001

1. Valid acc: 0.6913
2. Final test acc: 0.7108
3. Time: 128.48

# ============== 2 . 2 . c =================

## original (com overfit -> ver loss)

1. Training loss: 0.2175
2. Valid acc: 0.8582
3. Final Test acc: 0.7505

## L2 0.0001 (ainda com overfit -> L2 muito pequeno)

1. Training loss: 0.2734
2. Valid acc: 0.8527
3. Final Test acc: 0.7599


## Droupout (atenua muito o overfit)

1. Training loss: 0.3677
2. Valid acc: 0.8554
3. Final Test acc: 0.8034