import numpy as np

Vg_hom = 0.4 


rng = np.random.default_rng()
anc_freqs = rng.uniform(0.2,0.8, 100)
sub_freqs = rng.beta(anc_freqs, 1-anc_freqs, size=(2, 100))
sub_freqs[abs(sub_freqs - 0.5) > 0.3] = 0.8

tau = anc_freqs * (1-sub_freqs) ** (-1)
tau_sub = sub_freqs* ( 1-sub_freqs) **(-1)
var_gb = Vg_hom / sub_freqs[]




# Tune weights for tau
c.list = seq(-10, 10, length.out=1000)
    c.res = NULL
    
for(j in c.list){
    c=j
    tau2.test = c * tau2.raw
    var_gb = Vg_hom / m * sum(var1*tau2.test) # tune C so that Vg_hom = 0.4
    c.res = rbind(c.res, c(c, var_gb))
}
    
c.res = data.table( c.res)
    colnames(c.res) = c("c","Var")
    c.chosen  = c.res[which.min(abs(Var-Var.G1B))] # find which c gives value most close to the desired Var.GB
    c = c.chosen$c
    tau2 = c * tau2.raw # tau calcualted from combined AF although c is tuned to produce h2= 0.5 for the 1st ancestry group
    Var.GB.exp = Vg_hom / m * sum(var*tau2)
    Var.G1B.exp = Vg_hom / m * sum(var1*tau2) # Var.G1B.exp should be similar to Var.G2B.exp
    Var.G2B.exp = Vg_hom / m * sum(var2*tau2)
    

# Tune tau2 for Vg_1
c1.list = seq(-10, 10, length.out=1000)
c1.res = NULL
    
for( j in c1.list){    

    c1=j
    tau2.anc1.test = c1 * tau2.anc1.raw
    var_zg1m_1= Vg_1 / m * sum(var1*tau2.anc1.test) # want them to be Vg_1
    c1.res = rbind(c1.res, c(c1, var_zg1m_1))
}
    c1.res = data.table( c1.res)
    colnames(c1.res) = c("c1","Var")
    c1.chosen  = c1.res[which.min(abs(Var-Var.ZG1M_1))] # find which c gives value closest to the desired Var.ZG1M_1 = 0.2
    c1 = c1.chosen$c1
    tau2.anc1 = c1 * tau2.anc1.raw
    Var.ZG1M_1.exp = c1.chosen$Var
    Var.ZGM1.exp = Vg_1 / m * sum(var1.z*tau2.anc1)
    
# Tune tau2 for Vg_2
c2.list = seq(-10, 10, length.out=1000)
c2.res = NULL
    
for( j in c2.list){
    c2=j
    tau2.anc2.test = c2 * tau2.anc2.raw
    var_zgm2_2 = Vg_2 / m * sum(var2*tau2.anc2.test)
    c2.res = rbind(c2.res, c(c2, var_zgm2_2))
}
    
    c2.res = data.table( c2.res)
    colnames(c2.res) = c("c2","Var")
    c2.chosen  = c2.res[which.min(abs(Var-Var.ZG2M_2))] # find which c gives value most close to the desired Var.ZG2
    c2 = c2.chosen$c2
    tau2.anc2 = c2 * tau2.anc2.raw
    Var.ZG2M_2.exp = c2.chosen$Var
    Var.ZGM2.exp = Vg_2 / m * sum(var2.z*tau2.anc2)
    
variances = cbind( tau2*Vg_hom, tau2.anc1*Vg_1, tau2.anc2*Vg_2 )
variances.mean = apply(variances,2, mean)
variances2 = cbind( sd1*sd2*tau2*Vg_hom, var1*tau2*Vg_hom, var1*tau2.anc1*Vg_1, var2*tau2*Vg_hom, var2*tau2.anc2*Vg_2 ) # to calculate rg
variances.mean2 = apply(variances2,2, mean)
get_rg = function(x) { x[1]/{ sqrt( x[1] + x[2] )* sqrt( x[1] + x[3]) } }
rg.e = get_rg(variances.mean) # genetic effect cor
get_rg2 = function(x) { x[1]/{ sqrt( x[2] + x[3] )* sqrt( x[4] + x[5]) } }
rg.i = get_rg2(variances.mean2) # genetic impact cor
rg.e.all = cbind(rg.e.all, rg.e)
rg.i.all = cbind(rg.i.all, rg.i)
    
### Draw phenotypes

# Create beta, gamma1, gamma2
set.seed(i)
cov = diag(Vg_hom*tau2/m)
betas = mvrnorm(1, rep(0,1000), cov)
    
cov1 = diag(Vg_1*tau2.anc1/m)
gamma1 = mvrnorm(1, rep(0,1000), cov1)
    
cov2 = diag(Vg_2*tau2.anc2/m)
gamma2 = mvrnorm(1, rep(0,1000), cov2)
    
# Draw phenotype
set.seed(i)

G_hom = anc1.anc2.geno %*% betas # Shared genetic part: var(G_hom) should be close to Vg_1 or Var.GB
G1 = c( anc1.geno %*% gamma1, rep(0,2000))  # Anc1 specific genetics part: should be 2*Vg_1
G2 = c( rep(0,2000), anc2.geno %*% gamma2 ) # Anc2 specific genetics part:  should be 2*Vg_2
delta1 = c( rnorm(nrow(anc1.geno), 0, sqrt(Ve1) ), rep(0,2000)) # Anc1 specific error
delta2 = c( rep(0, 2000), rnorm(nrow(anc2.geno), 0, sqrt(Ve2) )) # Anc2 specific error
e = rnorm(nrow(anc1.anc2.geno), 0, sqrt(Ve)) # common error
intercept = c( rep(0,2000), rep(1,2000))
    
